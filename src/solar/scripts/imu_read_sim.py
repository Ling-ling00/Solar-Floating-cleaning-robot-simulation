#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
import numpy as np
import time


class IMUNode(Node):
    def __init__(self):
        super().__init__('imu_node')

        #subscription
        self.create_subscription(Imu, "/imu/out", self.imu_callback, 10)

        #publisher
        self.imu_publisher = self.create_publisher(Vector3, '/angle', 10)

        self.angle = [0.0, 0.0]
        self.time = [time.time(), time.time()]
        self.K = np.array([[0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0]]) #Kalman gain
        self.Xp = np.array([[0.0], [0.0], [0.0], [0.0]]) #Predicted state
        self.Xc = np.array([[0.0], [0.0], [0.0], [0.0]]) #Corrected state
        self.Pp = np.array([[0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0]]) #Predicted covariance
        self.Pc = np.array([[0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0]]) #Corrected covariance
        self.Yp = np.array([[0.0], [0.0]]) #Predicted measurement
        self.e = np.array([[0.0], [0.0]]) #Error

    def imu_callback(self, msg:Imu):
        U = np.array([[msg.angular_velocity.x], [msg.angular_velocity.y]])
        Y = np.array([[0],[0]])
        Y[0][0] = np.atan2(msg.linear_acceleration.y, msg.linear_acceleration.z)
        temp = np.sqrt((msg.linear_acceleration.y**2)+(msg.linear_acceleration.z**2))
        Y[1][0] = np.atan2(-msg.linear_acceleration.x, temp)
        self.time[0] = self.time[1]
        self.time[1] = time.time()
        self.kalman_filter(U, Y, self.time[1]-self.time[0])
        self.angle[0] = self.Xc[0][0]
        self.angle[1] = self.Xc[1][0]
        pub_msg = Vector3()
        pub_msg.x = self.angle[0]
        pub_msg.y = self.angle[1]
        print("roll angle:", self.angle[0])
        print("pitch angle:", self.angle[1])
        if self.angle[0] > 0.001:
            print("-------------------------in hole-------------------------------")
        print("\n")
        self.imu_publisher.publish(pub_msg)

    def kalman_filter(self,u, y, dt):
        A = np.array([[1, 0, -dt, 0],
                      [0, 1, 0, -dt],
                      [0, 0, 1, 0],
                      [0, 0, 1, 0]])
        B = np.array([[dt, 0],
                      [0, dt],
                      [0, 0],
                      [0, 0]])
        C = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])
        I = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        
        Q = np.array([[0.005, 0, 0, 0],
                      [0, 0.005, 0, 0],
                      [0, 0, 0.005, 0.005],
                      [0, 0, 0.005, 0.005]])
        R = np.array([[0.005, 0],
                      [0, 0.005]])
        
        #calculate kalman gain
        self.K = np.matmul(self.Pp, np.matmul(np.transpose(C), np.linalg.inv(np.add(np.matmul(C, np.matmul(self.Pp, np.transpose(C))),R))))

        #Predict the measurement
        self.Yp = np.matmul(C, self.Xp)

        #Calculate error
        self.e = y - self.Yp

        #Corrected state
        self.Xc = np.add(self.Xp, np.matmul(self.K, self.e))

        #Update covariance P
        self.Pc = np.matmul((I-np.matmul(self.K, C)), self.Pp)

        #Prediction step
        self.Xp = np.add(np.matmul(A, self.Xc), np.matmul(B, u))

        #Update covariance Pp
        self.Pp = np.add(np.matmul(np.matmul(A, self.Pc), np.transpose(A)), Q)

def main(args=None):
    rclpy.init(args=args)
    node = IMUNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()

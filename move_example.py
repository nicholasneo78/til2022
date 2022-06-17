from robomaster import robot
import cv2

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta", sn="3JKDH2T0014VYK")
    
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=True)

    ep_chassis = ep_robot.chassis

    x_val = 0.5
    y_val = 0.6
    z_val = 90

    # 前进 0.5米
    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

    # 后退 0.5米
    ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

    ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
    
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite("lol.jpg", img)

    # 左移 0.6米
    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()

     ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()

    # 右移 0.6米
    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite("lol2.jpg", img)


    # 左转 90度
    ep_chassis.move(x=0, y=0, z=z_val, z_speed=45).wait_for_completed()

    ep_chassis.move(x=0, y=y_val, z=z_val, z_speed=30).wait_for_completed()
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite("lol3.jpg", img)

    # 右转 90度
    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite("lol4.jpg", img)

    ep_robot.close()

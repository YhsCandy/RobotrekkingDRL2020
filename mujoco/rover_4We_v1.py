'''
Arquivo de configuração do ambient rover do mujoco

Endereço do arquivo : gym/gym/envs/mujoco

Baseado em: https://github.com/openai/gym/tree/master/gym/envs/mujoco

rover-4-wheels-diff-ackerman-double-front-wheel.xml qpos and qvel

body names:     ['rover', 'r-l-wheel', 'r-r-wheel', 'ghost-steer-wheel', 'f-l-wheel', 'f-l-axis', 'f-l-l-wheel', 'f-l-r-wheel', 'f-r-wheel', 'f-r-axis', 'f-r-l-wheel', 'f-r-r-wheel']
body id:        [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
body_geomadr:   [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

qpos[0] = rover's x position
qpos[1] = rover's y position
qpos[2] = rover's z position
qpos[3] = rover's w quaternion vector
qpos[4] = rover's a quaternion vector
qpos[5] = rover's b quaternion vector
qpos[6] = rover's c quaternion vector
qpos[7] = rear left wheel rotation angle
qpos[8] = rear right wheel rotation angle
qpos[9] = ghost steer hinge
qpos[10]= front left wheel steer angle
qpos[11]= front left wheel rotation 1 angle
qpos[12]= front left wheel rotation 2 angle
qpos[13]= front right wheel steer angle
qpos[14]= front right wheel rotation 3 angle
qpos[15]= front right wheel rotation 4 angle

qvel[0] = rover's x velocity
qvel[1] = rover's y velocity
qvel[2] = rover's z velocity
qvel[3] = rover's x angular velocity
qvel[4] = rover's y angular velocity
qvel[5] = rover's z angular velocity
qvel[6] = rear left wheel angular velocity
qvel[7] = rear right wheel angular velocity
qvel[8] = ghost steer hinge velocity
qvel[9]= front left wheel steer velocity
qvel[10]= front left wheel rotation 1 velocity
qvel[11]= front left wheel rotation 2 velocity
qvel[12]= front right wheel steer velocity
qvel[13]= front right wheel rotation 3 velocity
qvel[14]= front right wheel rotation 4 velocity



rover-4-wheels.xml qpos and qvel

qpos[0] = rover's x position
qpos[1] = rover's y position
qpos[2] = rover's z position
qpos[3] = rover's w quaternion vector
qpos[4] = rover's a quaternion vector
qpos[5] = rover's b quaternion vector
qpos[6] = rover's c quaternion vector
qpos[7] = rear left wheel rotation angle
qpos[8] = rear right wheel rotation angle
qpos[9] = steerbar rotation angle
qpos[10]= front left wheel rotation angle
qpos[11]= front right wheel rotation angle
qpos[12]= drive motor rotation angle (the prism between rear wheels)

qvel[0] = rover's x velocity
qvel[1] = rover's y velocity
qvel[2] = rover's z velocity
qvel[3] = rover's x angular velocity
qvel[4] = rover's y angular velocity
qvel[5] = rover's z angular velocity
qvel[6] = rear left wheel angular velocity
qvel[7] = rear right wheel angular velocity
qvel[8] = steerbar angular velocity
qvel[9]= front left wheel angular velocity
qvel[10]= front right wheel angular velocity
qvel[11]= drive motor angular velocity (the prism between rear wheels)


rover-4-wheels_loose.xml qpos and qvel

qpos[0] = rover's x position
qpos[1] = rover's y position
qpos[2] = rover's z position
qpos[3] = rover's w quaternion vector
qpos[4] = rover's a quaternion vector
qpos[5] = rover's b quaternion vector
qpos[6] = rover's c quaternion vector
qpos[7] = rear left wheel steer rotation angle		(very limited)
qpos[8] = rear left wheel rolling rotation angle
qpos[9] = rear right wheel steer rotation angle		(very limited)
qpos[10]= rear right wheel rolling rotation angle
qpos[11]= front left wheel steer rotation angle
qpos[12]= front left wheel rolling rotation angle
qpos[13]= front right wheel steer rotation angle
qpos[14]= front right wheel rolling rotation angle

qvel[0] = rover's x velocity
qvel[1] = rover's y velocity
qvel[2] = rover's z velocity
qvel[3] = rover's x angular velocity
qvel[4] = rover's y angular velocity
qvel[5] = rover's z angular velocity
qvel[6] = rear left wheel steer angular velocity
qvel[7] = rear left wheel rolling angular velocity
qvel[8] = rear right wheel steer angular velocity
qvel[9]= rear right wheel rolling angular velocity
qvel[10]= front left wheel steer angular velocity
qvel[11]= front left wheel rolling angular velocity
qvel[12]= front right wheel steer angular velocity
qvel[13]= front right wheel rolling angular velocity

'''

import numpy as np
import cv2
from gym import utils
from gym.envs.mujoco import mujoco_env
from gym import spaces
import matplotlib.pyplot as plt
import mujoco_py
import spinup.utils.logx as logx

# o campo é tem dimensoes (x,y)=(44,25) [metros]
# É uma matriz (x,y) de (0,0) até (3, 4) elementos em que cada elemento tem dimensão (x,y) de (44/4, 25/5) = (11.0 , 5.0) [metros]
# Na configuração A, os elementos (2, 1) e (2, 3) tem obstáculos
# Na configuração B, os elementos (1, 2) e (3, 2) tem obstáculos

class RoverRobotrek4Wev1Env(mujoco_env.MujocoEnv, utils.EzPickle):
    # EXPERIMENTS LOG PARAMETERS #
    loose_version = False
    ackerman_version = True
    original_field = False
    use_ramps = True
    use_posts = True
    reduced_obs = False
    flip_penalising = True
    flipped_time = 2.0
    death_circle_penalising = True
    death_circ_dist = 0.8
    death_circ_time = 8
    fwd_rew = 0.1
    control_cost = 0.0007
    svv_rew = 0.0001
    time_pnlt = 0.00012
    leave_penalty = 10
    # max_accxy = 100.0
    # max_accz = 50.0
    max_accxy = 500.0
    max_accz = 500.0
    colision_penalty = 10
    bumpiness_penalty = 1
    circle_pnlt = 10
    flip_pnlt = 10
    goal_rwd = 1
    gps_error = 0.00  # Erro gaussiano do GPS
    im_size = (440, 270)  # tamanho da imagem adquirida pelo mujoco
    img_reduced_size = (128, 128)  # tamanho da imagem reduzida

    # if start_at_initpos is True, random_start is not used.
    # if start_at_initpos is False, random_start is used.
    start_at_initpos = False

    # about random_start(rs) and random_current_goal(rcg)
    # rs True  and rcg True : rover starts (almost) anywhere and has a random goal (0, 1 or 2)
    # rs True  and rcg False: rover starts (almost) anywhere and has as current_goal the first goal (0)
    # rs False and rcg True : rover starts at the goal before its current_goal (and this one is random: 0, 1 or 2)
    # rs False and rcg False: rover starts at the goal before its current_goal (and this one is the first goal: 0)
    random_start = False
    random_current_goal = False
    avoid_radius = 0.5 # radius for obstacle avoidance in rover's position randomizer

    # defines if the episode will end after current_goal is reached
    end_after_current_goal = False

    current_obstacle_setup = None
    current_goal = 0  # inicializa a variável do objetivo atual
    x_before = [0, 0]  # Inicializa o vetor estado do carrinho [posição, orientação]
    is_cam = False
    last_15_pos = np.array([3, 3])
    last_15_time = 0
    last_straight_time = 0
    if reduced_obs:
        obs_size = (5,)
    elif loose_version:
        obs_size = (16,)
    else:
        obs_size = (14,)

    initial_pos_A = ((22.5, 15.5, 0), (22.5, 5.5, 0))
    initial_pos_B = ((11.5, 10.5, 0), (33.5, 10.5, 0))

    # block_step = 1

    long_bump_store = []
    long_bump_used = []

    circular_bump_store = []
    circular_bump_used = []

    square_long_hole_store = []
    square_long_hole_used = []

    square_hole_store = []
    square_hole_used = []

    box_tile_store = []
    box_tile_used = []


    ramp_store = []
    ramp_used = []


    post_store = []
    post_used = []

    useds_lists_list = [long_bump_used, circular_bump_used, square_long_hole_used, square_hole_used, box_tile_used,
                        ramp_used, post_used]
    store_lists_list = [long_bump_store, circular_bump_store, square_long_hole_store, square_hole_store, box_tile_store,
                        ramp_store, post_store]

    camera_renderer = None
    camera_id = None
    flag_render = False
    save_images = False

    def __init__(self):

        if self.random_current_goal:
            self.randomize_current_goal()

        if not self.loose_version:
            if self.ackerman_version:
                mujoco_env.MujocoEnv.__init__(self, 'Rover4We-v1/main-trekking-challenge-4wheels_diff-acker-double-front-wheel.xml',
                                      4)
            else:
                # mujoco_env.MujocoEnv.__init__(self, 'Rover4We-v1/main-trekking-challenge-4wheelsv1.xml',
                mujoco_env.MujocoEnv.__init__(self, 'Rover4We-v1/main-trekking-challenge-4wheels_diff.xml',
                                      4)  # __init__(self, model_path, frame_skip):
        else:
            mujoco_env.MujocoEnv.__init__(self, 'Rover4We-v1/main-trekking-challenge-4wheels_loosev1.xml',
                                          4)  # __init__(self, model_path, frame_skip):
        utils.EzPickle.__init__(self)
        self.observation_space = spaces.Box(shape=self.obs_size, low=0, high=0)

        for body in self.sim.model.body_names:
            if body[0:8] == 'long-bum':
                self.long_bump_store.append(self.sim.model.body_name2id(body))

            if body[0:8] == 'circ-bum':
                self.circular_bump_store.append(self.sim.model.body_name2id(body))

            if body[0:8] == 'square-l':
                self.square_long_hole_store.append(self.sim.model.body_name2id(body))

            if body[0:8] == 'square-h':
                self.square_hole_store.append(self.sim.model.body_name2id(body))

            if body[0:8] == 'box-tile':
                self.box_tile_store.append(self.sim.model.body_name2id(body))

            if body[0:4] == 'ramp':
                self.ramp_store.append(self.sim.model.body_name2id(body))

            if body[0:4] == 'post':
                self.post_store.append(self.sim.model.body_name2id(body))

        self.holes = np.zeros((2, 11, 5))
        self.map_generator()
        self.camera_renderer = mujoco_py.MjRenderContextOffscreen(self.sim)
        self.camera_id = self.sim.model.camera_name2id('first-person')

    def camera_renderer_initializer(self):
        self.camera_renderer = mujoco_py.MjRenderContextOffscreen(self.sim)

    def camera_rendering(self, width, height, cam_id):
        self.camera_renderer.render(width=width, height=height, camera_id=cam_id)
        self.camera_renderer.render(width=width, height=height, camera_id=cam_id) #precisa renderizar 2x pra ficar bom
        img = self.camera_renderer.read_pixels(width, height, False)
        return img

    def step(self, action):
        '''
        Step da simulação : são definidos o observation_state, o reward e se o episódio terminou 
        '''

        x_before = self.x_before  # salva o vetor estado anterior
        '''
        For regular version: action[0] = steering_torque, action[1] = traction_torque
        For loose version: action[0] = steering_torque, action[1] = traction_torque
        '''
        self.do_simulation(action, self.frame_skip)

        gps_exact, ob, img = self._get_obs()  # obtém a posição real do carrinho, os dados dos sensores e a imagem 

        x_after = ob[0:2]  # vetor estado do carrinho [gps_sensor_x, gps_sensor_y]

        cur_goal = ob[-5:-3]  # Objetivo atual [coordinate_goal_x, coordinate_goal_y]

        # Cálculo da reward pela trajetória
        desired_trajectory = cur_goal - x_before
        performed_trajectory = x_after - x_before
        forward_reward = self.fwd_rew * np.dot(performed_trajectory, desired_trajectory) / (
                    np.sqrt(np.square(desired_trajectory).sum()) * self.dt)

        # Cálculo do custo de controle
        if self.loose_version:
            ctrl_cost = self.control_cost * np.square(action).sum()
        else:
            ctrl_cost = self.control_cost * np.square(action[1])

        # Cálculo da reward de sobrevivência
        # survive_reward = self.svv_rew
        time_cost = self.time_pnlt

        # Atualiza o vetor de estado do carrinho
        self.x_before = x_after

        # Verifica se o carrinho está sobre a base e acende a luz
        on_base, n_spot = self.line_reader(gps_exact)
        lamp_state = self.sim.model.light_active[1]
        goal, on_base = self.is_in_goal(gps_exact)

        if goal:
            self.sim.model.light_active[1] = 1
            self.update_goal()
            goal_reward = self.goal_rwd
        else:
            goal_reward = 0
            if not on_base:
                self.sim.model.light_active[1] = 0
                # self.just_reached_goal = False

        # Soma todas as rewards e custos
        # r = survive_reward + forward_reward - ctrl_cost + goal_reward
        r = forward_reward - ctrl_cost - time_cost + goal_reward
        # Atualização da reward caso o carrinho termine a prova ou de penalidades caso o carrinho deixe o campo (dá pra tacar numa função isso aqui)
        if (self.current_goal == -1):
            done = True
            # r = r + 20
        elif (gps_exact[0] < 0) or (gps_exact[1] < 0) or (gps_exact[0] > 44) or (
                gps_exact[1] > 25):  # penalty for leaving the camp
            done = True
            r -= self.leave_penalty
        elif self.sim.data.time >= 99.9:
            done = True

        else:
            done = False

        if self.end_after_current_goal and goal:
            done = True

        self.last_15_pos, self.last_15_time, done, circle_penalty = self.death_circle(self.death_circ_dist,
                                                                      self.death_circ_time, x_after, self.last_15_pos,
                                                                      self.sim.data.time, self.last_15_time, done)
        if self.death_circle_penalising:
            r -= circle_penalty
        self.last_straight_time, done, flip_penalty = self.is_flipped(done, self.sim.data.time, self.last_straight_time,
                                                                      self.flipped_time)
        if self.flip_penalising:
            r -= flip_penalty

        if self.sim.data.time > 2: # avoid initial falling
            colision, bumpiness = self.colision_detector(self.max_accxy, self.max_accz)
            if colision:
                r -= self.colision_penalty
            elif bumpiness:
                r -= self.bumpiness_penalty

        if self.reduced_obs == True:
            return np.asarray([np.concatenate([ob[:2],ob[-3:]]), img]), r, done, {}
            # return np.asarray([ob[-3:], img]), r, done, {}
        else:
            return np.asarray([ob, img]), r, done, {}

    def is_flipped(self, done, current_time, last_straight_time, death_time):

        rr_wheel_zpos = self.sim.data.get_body_xpos('r-r-wheel')[2]
        rl_wheel_zpos = self.sim.data.get_body_xpos('r-l-wheel')[2]
        if not self.loose_version:
            fr_wheel_zpos = self.sim.data.get_body_xpos('f-r-wheel')[2]
            fl_wheel_zpos = self.sim.data.get_body_xpos('f-l-wheel')[2]
        else:
            fr_wheel_zpos = self.sim.data.get_body_xpos('steer-r-wheel')[2]
            fl_wheel_zpos = self.sim.data.get_body_xpos('steer-l-wheel')[2]

        rover_centroid_zpos = self.sim.data.body_xpos[1][2]

        diff_rr = rover_centroid_zpos - rr_wheel_zpos
        diff_rl = rover_centroid_zpos - rl_wheel_zpos
        diff_fr = rover_centroid_zpos - fr_wheel_zpos
        diff_fl = rover_centroid_zpos - fl_wheel_zpos
        flip_penalty = 0

        if diff_rr < 0 or diff_rl < 0 or diff_fr < 0 or diff_fl < 0:
            if current_time - last_straight_time > death_time:
                done = True
                flip_penalty = self.flip_pnlt
        else:
            last_straight_time = current_time
        return last_straight_time, done, flip_penalty

    def death_circle(self, death_radius, death_time, current_position, last_position, current_time, last_time, done):

        distance = np.linalg.norm(current_position - last_position)
        circle_penalty = 0
        if distance > death_radius:
            if current_time - last_time < death_time:
                last_position = current_position
                last_time = current_time

                # print('atualizando posicao de 1.5m:', self.last_15_pos, 'tempo:', self.last_15_time)
        else:
            if current_time - last_time > death_time:
                done = True
                circle_penalty = self.circle_pnlt
                # print('dead: ficou muito tempo parado. death time:', current_time)

        return last_position, last_time, done, circle_penalty

    def colision_detector(self, max_accxy, max_accz):
        acc_vec = self.sim.data.qacc[:3] # [ax, ay, az]
        accxy = np.sqrt(acc_vec[0]**2 + acc_vec[1]**2)
        daccz = np.abs(acc_vec[2])
        if accxy >= max_accxy:
            print("Colisao detectada: {}".format(accxy))
            return True, False
        elif daccz >= self.max_accz:
            print("Buraqueira detectada: {}".format(daccz))
            return False, True
        else:
            return False, False

    def is_in_goal(self, gps_exact):
        on_base, n_spot = self.line_reader(gps_exact)
        if on_base and n_spot == self.current_goal:
            return True, on_base
        else:
            return False, on_base

    def _get_obs(self):
        '''
        Função que retorna os dados do observation_state
        '''
        # gps exato
        gps_exact = self.sim.data.body_xpos[1][0:2].copy()
        # vel exata
        speed_exact = [self.sim.data.qvel[0:2]].copy()

        # gps sensor com erro
        gps_sensor = gps_exact + self.gps_error * np.random.rand(2)
        # vel sensor com erro
        speed_sensor = np.asarray(speed_exact) # + self.gps_error * np.random.rand(2)

        # orientation_rover
        orientation_rover = self.sim.data.body_xmat[1][0:2].copy()
        rover_ang_speed = self.sim.data.qvel[5]
        if not self.loose_version:
            if self.ackerman_version:
                ghost_steer_angle = self.sim.data.qpos[9]
                ghost_steer_angspeed = self.sim.data.qvel[8]
            else:
                steer_bar_angle = self.sim.data.qpos[9]
                steer_bar_angspeed = self.sim.data.qvel[8]
        else: #
            steer_r_wheel_angle = self.sim.data.qpos[13]
            steer_r_wheel_angspeed = self.sim.data.qvel[12]
            steer_l_wheel_angle = self.sim.data.qpos[11]
            steer_l_wheel_angspeed = self.sim.data.qvel[10]

        # camera
        if not self.is_cam:
            self.sim.render(
                mode='window')  # , camera_name='first-person', width=im_size[0], height=im_size[1], depth=False)
            self.is_cam = True
        if self.camera_renderer is None:
            gray = np.zeros(shape=self.img_reduced_size)
            self.camera_renderer_initializer()
        else:
            img = self.camera_rendering(width=self.im_size[0], height=self.im_size[1], cam_id=self.camera_id)
            if self.save_images: cv2.imwrite("./running_images/full_size_{:0>7.3f}.png".format(self.sim.data.time), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            img = cv2.resize(img, self.img_reduced_size)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            if self.save_images: cv2.imwrite("./running_images/reduced_size_{:0>7.3f}.png".format(self.sim.data.time), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            if self.save_images: cv2.imwrite("./running_images/reduced_gray_{:0>7.3f}.png".format(self.sim.data.time), gray)

        if self.current_goal == 0:
            coordinates_goal = np.asarray([40, 20])
            goal = np.asarray([0, 0, 1])
        elif self.current_goal == 1:
            coordinates_goal = np.asarray([30, 2])
            goal = np.asarray([0, 1, 0])
        elif self.current_goal == 2:
            coordinates_goal = np.asarray([6, 18])
            goal = np.asarray([1, 0, 0])
        elif self.current_goal == -1:
            coordinates_goal = np.asarray([0, 0])
            goal = np.asarray([0, 0, 0])

        if not self.loose_version:
            if self.ackerman_version:
                return gps_exact, np.concatenate(
                    [gps_sensor.flat, orientation_rover.flat, [ghost_steer_angle], speed_sensor.flat, [rover_ang_speed],
                     [ghost_steer_angspeed], coordinates_goal.flat, goal.flat]), gray / 255.0
            else:
                return gps_exact, np.concatenate(
                    [gps_sensor.flat, orientation_rover.flat, [steer_bar_angle], speed_sensor.flat, [rover_ang_speed],
                     [steer_bar_angspeed], coordinates_goal.flat, goal.flat]), gray / 255.0

        else:
            return gps_exact, np.concatenate(
                [gps_sensor.flat, orientation_rover.flat, [steer_r_wheel_angle], [steer_l_wheel_angle], speed_sensor.flat, [rover_ang_speed],
                 [steer_r_wheel_angspeed], [steer_l_wheel_angspeed], coordinates_goal.flat, goal.flat]), gray / 255.0

        '''return gps_exact, np.concatenate(
            [gps_sensor.flat, orientation_rover.flat, [steer_bar_angle], speed_sensor.flat, [rover_ang_speed],
             [steer_bar_angspeed], coordinates_goal.flat, goal.flat]), gray / 255.0'''

    def render(self):
        self._get_viewer('human').render()
        if self.flag_render == False:
            self.camera_renderer_initializer()
            self.flag_render = True

    def reset_model(self):
        '''
        Reinicializa a simulação
        '''
        if not self.original_field:
            self.map_reset()

        self.map_generator()

        if self.random_current_goal:
            self.randomize_current_goal()
        else:
            self.current_goal = 0

        if self.start_at_initpos:
            self.set_state(self.init_qpos, self.init_qvel)
        else:
            if self.random_start:
                bad_position = True
                while bad_position:
                    bad_position = False
                    rover_random_xy_pos = np.asarray([np.random.rand()*44, np.random.rand()*25])
                    # rover_random_xy_pos = self.sim.model.body_pos[self.ramp_used[0]][0:2]
                    print('new position: {}'.format(rover_random_xy_pos))
                    if self.current_obstacle_setup == 'A' and ((11-self.avoid_radius <= rover_random_xy_pos[0] <= 22+self.avoid_radius and 10-self.avoid_radius <= rover_random_xy_pos[1] <= 15+self.avoid_radius) or (33-self.avoid_radius <= rover_random_xy_pos[0] <= 44+self.avoid_radius and 10-self.avoid_radius <= rover_random_xy_pos[1] <= 15+self.avoid_radius)):
                        bad_position = True
                        print('cant: collision with "A" obstacles')
                        continue
                    if self.current_obstacle_setup == 'B' and ((22-self.avoid_radius <= rover_random_xy_pos[0] <= 33+self.avoid_radius and  5-self.avoid_radius <= rover_random_xy_pos[1] <= 10+self.avoid_radius) or (22-self.avoid_radius <= rover_random_xy_pos[0] <= 33+self.avoid_radius and 15-self.avoid_radius <= rover_random_xy_pos[1] <= 20+self.avoid_radius)):
                        bad_position = True
                        print('cant: collision with "B" obstacles')
                        continue

                    for ramp in self.ramp_used:
                        if np.sqrt((self.sim.model.body_pos[ramp][0]-rover_random_xy_pos[0])**2 + (self.sim.model.body_pos[ramp][1]-rover_random_xy_pos[1])**2) < (np.sqrt(2)+self.avoid_radius):
                            bad_position = True
                            print('cant: collision between rover and ramp {}'.format(ramp))
                            break
                    if bad_position:
                        continue

                    for post in self.post_used:
                        if np.sqrt((self.sim.model.body_pos[post][0]-rover_random_xy_pos[0])**2 + (self.sim.model.body_pos[post][1]-rover_random_xy_pos[1])**2) < (0.15+self.avoid_radius):
                            bad_position = True
                            print('cant: collision between rover and post {}'.format(post))
                            break
                    if bad_position:
                        continue

                    # for contact in self.sim.data.contact:
                    #     for obstacle_body in iter([*self.ramp_used, *self.post_used]): # concat ramp_used and post_used (iter is nor necessary, perhaps)
                    #         if contact.geom1 == self.sim.model.body_geomadr[obstacle_body]:
                    #             if 20 <= contact.geom2 <= 31: # 20 to 31 are rover's geoms
                    #                 bad_position = True
                    #                 print('cant: collision between rover (geom {}) and {} (geom {})'.format(contact.geom2, self.sim.model.body_id2name(obstacle_body), contact.geom1))
                    #                 continue
                    #         elif contact.geom2 == self.sim.model.body_geomadr[obstacle_body]:
                    #             if 20 <= contact.geom1 <= 31: # 20 to 31 are rover's geoms
                    #                 bad_position = True
                    #                 print('cant: collision between rover (geom {}) and {} (geom {})'.format(contact.geom1, self.sim.model.body_id2name(obstacle_body), contact.geom2))
                    #                 continue
                print(logx.colorize("starting at random position {}".format(rover_random_xy_pos), 'blue', bold=False))
                # print('current_goal: {}'.format(self.current_goal))
                quat = create_quat(np.random.rand()*2*np.pi, 0, 0, 1, is_radian=True)
                self.set_state(np.array([*rover_random_xy_pos, 0.2, *quat, *self.init_qpos[7:]]), self.init_qvel)
                #self.set_state(np.array([*(self.sim.model.body_pos[self.ramp_used[0]][0:2]), 0.200, *self.init_qpos[3:]]), self.init_qvel)
            else:
                if self.current_goal < 1:
                    self.set_state(self.init_qpos, self.init_qvel)
                else:
                    quat = create_quat(np.random.rand()*2*np.pi, 0, 0, 1, is_radian=True)
                    init_xy_rover = self.get_goal_xy_position(self.current_goal - 1)
                    self.set_state(np.asarray([init_xy_rover[0], init_xy_rover[1], 0.2, *quat, *self.init_qpos[7:]]), self.init_qvel)

                print(logx.colorize("starting at {}".format('init_pos' if self.current_goal == 0 else 'goal {}'.format(self.current_goal-1)), 'cyan', bold=False))

        print(logx.colorize('current_goal: {}'.format(self.current_goal), 'yellow', bold=False))

        # self.just_reached_goal = False
        gps_exact, ob, img = self._get_obs()
        self.x_before = ob[0:2].copy() + self.gps_error * np.random.rand(2)

        self.last_15_pos = np.array([3, 3])
        self.last_15_time = 0

        if self.reduced_obs == True:
            return np.asarray([np.concatenate([ob[:2], ob[-3:]]), img])
            # return np.asarray([ob[-3:], img])
        else:
            return np.asarray([ob, img])

    def map_generator(self):
        # distribute hole fillers in original field
        if self.original_field:
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler1')] = np.asarray(self.initial_pos_B[0])
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler2')] = np.asarray(self.initial_pos_B[1])
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler3')] = np.asarray(self.initial_pos_A[0])
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler4')] = np.asarray(self.initial_pos_A[1])
            return

        # distribute posts
        if self.use_posts:
            goals = [(40, 20), (30, 2), (6, 18)]
            pos = [[(-1, -1), (-1, 0), (0, -1), (0, 1)], [(-1, 1), (-1, 0), (0, 1), (0, -1)],
                   [(1, -1), (1, 0), (0, -1), (0, 1)]]
            for index, goal in enumerate(goals):
                post = self.post_store.pop()
                np.random.shuffle(pos[index])
                posit = pos[index].pop()
                self.sim.model.body_pos[post] = np.asarray([goal[0] + posit[0], goal[1] + posit[1], 0])
                self.post_used.append(post)
                for i in range(2):
                    if np.random.choice([0, 1]) == 1:
                        post = self.post_store.pop()
                        posit = pos[index].pop()
                        self.sim.model.body_pos[post] = np.asarray([goal[0] + posit[0], goal[1] + posit[1], 0])
                        self.post_used.append(post)

        # distribute ramps
        if self.use_ramps:
            init_field_pos = (5.5, 2.5)
            fields = [(1, 0), (3, 0), (0, 1), (1, 1), (3, 1), (0, 2), (2, 2), (1, 3), (0, 4), (1, 4), (2, 4)]
            np.random.shuffle(fields)
            for i in range(len(self.ramp_store)):
                x = 9 * np.random.rand(1) - 4.5
                y = 3 * np.random.rand(1) - 1.5
                ramp_ = self.ramp_store.pop()
                field_ = fields.pop()
                self.sim.model.body_pos[ramp_] = np.asarray(
                    [init_field_pos[0] + field_[0] * 11 + x, init_field_pos[1] + field_[1] * 5 + y, 0])
                self.ramp_used.append(ramp_)
                orient = np.random.choice([0, 1, 2, 3])
                if orient == 0:
                    self.sim.model.body_quat[ramp_] = np.array([np.sqrt(2) / 2, 0, 0, np.sqrt(2) / 2])
                elif orient == 1:
                    self.sim.model.body_quat[ramp_] = np.array([np.sqrt(2) / 2, 0, 0, -np.sqrt(2) / 2])
                elif orient == 2:
                    self.sim.model.body_quat[ramp_] = np.array([0, 0, 0, 1])
                else:
                    self.sim.model.body_quat[ramp_] = np.array([1, 0, 0, 0])

        # distribute parts on holes
        allow_x_dir = True
        allow_y_dir = True

        self.current_obstacle_setup = np.random.choice(['A', 'B'])

        if self.current_obstacle_setup == 'A':
            init_pos = np.asarray(self.initial_pos_A)
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler1')] = np.asarray(self.initial_pos_B[0])
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler2')] = np.asarray(self.initial_pos_B[1])
        else:
            init_pos = np.asarray(self.initial_pos_B)
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler1')] = np.asarray(self.initial_pos_A[0])
            self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler2')] = np.asarray(self.initial_pos_A[1])

        for index_hole, hole in enumerate(self.holes):
            ip = np.asarray(init_pos[index_hole])
            for space_x in range(11):
                for space_y in range(5):

                    allowed_lists = []

                    # se o espaco nao estiver alocado
                    if hole[space_x, space_y] == False:
                        # se estiver no lado oposto a x, no fim
                        if space_x == hole.shape[0] - 1:
                            # nao pode usar long na direcao x
                            allow_x_dir = False
                        # se estiver no lado oposto a y, no fim
                        if space_y == hole.shape[1] - 1 or hole[space_x, space_y + 1] == True:
                            # nao pode usar long na direcao y
                            allow_y_dir = False

                        # se nao tiver elemento do respectivo tipo pra utilizar, sua lista nao sera adicionada a allowed_lists
                        # se nenuma direcao pode ser utilizada (por estar no fim do espaco), nenhum long pode ser escolhido
                        probability = []
                        count_longs = 0
                        count_shorts = 0
                        long_prob_balance = .10
                        if allow_x_dir or allow_y_dir:
                            if not len(self.long_bump_store) == 0:
                                allowed_lists.append(self.long_bump_store)
                                count_longs = count_longs + 1
                            if not len(self.square_long_hole_store) == 0:
                                allowed_lists.append(self.square_long_hole_store)
                                count_longs = count_longs + 1

                        if not len(self.circular_bump_store) == 0:
                            allowed_lists.append(self.circular_bump_store)
                            count_shorts = count_shorts + 1
                        if not len(self.square_hole_store) == 0:
                            allowed_lists.append(self.square_hole_store)
                            count_shorts = count_shorts + 1
                        if not len(self.box_tile_store) == 0:
                            allowed_lists.append(self.box_tile_store)
                            count_shorts = count_shorts + 1

                        # print('long_bump_store',len(self.long_bump_store),
                        #       'square_long_hole_store',len(self.square_long_hole_store),
                        #       'circular_bump_store', len(self.circular_bump_store),
                        #       'square_hole_store', len(self.square_hole_store))

                        probability = np.ones(count_longs + count_shorts)

                        if not count_longs == 0:
                            probability[0:count_longs] *= long_prob_balance / count_longs
                            probability[count_longs:] *= (1 - long_prob_balance) / count_shorts
                        else:
                            probability = None

                        # print('probability', probability)

                        # guarda o tipo de objeto selecionado
                        # print('len(allowed_lists)',len(allowed_lists))
                        choosed_class = allowed_lists[np.random.choice(len(allowed_lists), p=probability)]

                        flag_list = 0

                        # populando as listas de used
                        if choosed_class == self.long_bump_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.long_bump_used.append(chosen_one)
                            flag_list = 1

                        elif choosed_class == self.square_long_hole_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.square_long_hole_used.append(chosen_one)
                            flag_list = 2

                        elif choosed_class == self.circular_bump_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.circular_bump_used.append(chosen_one)

                        elif choosed_class == self.square_hole_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.square_hole_used.append(chosen_one)

                        elif choosed_class == self.ramp_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.ramp_used.append(chosen_one)

                        elif choosed_class == self.box_tile_store:
                            chosen_one = choosed_class.pop()  # "captura" a peça escolhida
                            self.box_tile_used.append(chosen_one)

                        # se for long qualquer coisa, precisa aplicar rotacao
                        if flag_list == 1 or flag_list == 2:

                            if not allow_x_dir:
                                direction = 'y'
                            elif not allow_y_dir:
                                direction = 'x'
                            else:
                                direction = np.random.choice(['x', 'y'])

                            # print('direction',direction,'allow x',allow_x_dir,'allow y',allow_y_dir)

                            # ao rotacionar, ocupar o tile adjacente
                            if direction == 'x':
                                # a coisa esta na direcao x por padrao
                                hole[space_x + 1, space_y] = True
                            else:
                                # aplicar direcao y
                                hole[space_x, space_y + 1] = True
                                # rotacionando -90 na direcao z pra coisa ficar na direcao y
                                self.sim.model.body_quat[chosen_one] = np.array([np.sqrt(2) / 2, 0, 0, np.sqrt(2) / 2])

                        # aplica posicao
                        self.sim.model.body_pos[chosen_one] = ip + np.array([space_x, space_y, 0])
                        # declara o espaco como utilizado
                        hole[space_x, space_y] = True

                    # reseta as variaveis para a proxima iteracao
                    allow_x_dir = True
                    allow_y_dir = True

    def map_reset(self):
        self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler1')] = np.array([10, 10, -10])
        self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler2')] = np.array([10, 10, -10])
        self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler3')] = np.array([10, 10, -10])
        self.sim.model.body_pos[self.sim.model.body_name2id('hole_filler4')] = np.array([10, 10, -10])
        for index in range(len(self.useds_lists_list)):
            for elem_ in self.useds_lists_list[index]:
                self.sim.model.body_pos[elem_] = np.array([10, 10, -10])  # element behind field
                if (self.useds_lists_list[index] == self.long_bump_used
                        or self.useds_lists_list[index] == self.square_long_hole_used
                        or self.useds_lists_list[index] == self.ramp_used):  # rotates back long elements
                    self.sim.model.body_quat[elem_] = np.array([1., 0., 0., 0.])
            # print("store list",index,'before:',self.store_lists_list[index])
            self.store_lists_list[index] += self.useds_lists_list[index]  # merge lists
            # print("store list",index,'after:',self.store_lists_list[index])
            # print("used list",index,'before:',self.useds_lists_list[index])
            self.useds_lists_list[index].clear()  # clear useds list
            # print("used list",index,'after:',self.useds_lists_list[index])
            self.holes[:, :, :] = 0  # clear holes vector

    def viewer_setup(self):
        # Como a câmera vai ser renderizada
        v = self.viewer
        v.cam.trackbodyid = 0
        v.cam.distance = self.model.stat.extent * 0.85
        v.cam.lookat[2] = 0.12250000000000005  # v.model.stat.center[2]

    def update_goal(self):
        print(logx.colorize("Goal {} reached!".format(self.current_goal), 'red', bold=True))
        if self.current_goal != 2:
            self.current_goal += 1
        else:
            self.current_goal = -1
        print(logx.colorize("Next Goal: {}".format(self.current_goal), 'red', bold=True))

    def line_reader(self, gps_exact):
        '''
        Simulação do seguidor de linha
        
        Parâmetros de retorno:
            -> on_base = o sensor detectou que o rover se encontra em alguma base
            -> n_spot = qual base que o rover se encontra (apenas para atualiuzação do objetivo)
        '''
        if (39.5 <= gps_exact[0] <= 40.5) and (19.5 <= gps_exact[1] <= 20.5):
            return 1, 0
        elif (29.5 <= gps_exact[0] <= 30.5) and (1.5 <= gps_exact[1] <= 2.5):
            return 1, 1
        elif (5.5 <= gps_exact[0] <= 6.5) and (17.5 <= gps_exact[1] <= 18.5):
            return 1, 2
        else:
            return 0, -1

    def randomize_current_goal(self):
        self.current_goal = np.random.choice([0, 1, 2])

    def get_goal_xy_position(self, goal):
        pos = np.zeros(2)
        if goal == 0:
            pos[:] = [40.0, 20.0]
        elif goal == 1:
            pos[:] = [30.0, 2.0]
        elif goal == 2:
            pos[:] = [6.0, 18.0]
        else:
            raise Exception("required goal {} does not exist!".format(goal))
        return pos


def create_quat(angle, x, y, z, is_radian=True):
    dir = np.array([x, y, z])
    dir = dir/np.linalg.norm(dir)
    if is_radian:
        return np.array([np.cos(angle / 2), *(dir * np.sin(angle / 2))])
    else:
        angle = angle*np.pi/180
        return np.array([np.cos(angle / 2), *(dir * np.sin(angle / 2))])


def axisangle_from_quat(quat):
    angle_rad = 2*np.arccos(quat[0])
    dir = quat[1:]/(np.arc(2*angle_rad))
    return (angle_rad, dir)


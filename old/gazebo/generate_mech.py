#!/usr/bin/python

import math

CHASSIS_LENGTH = 0.19
CHASSIS_MASS = 1.05
COXA_LENGTH = 0.06
FEMUR_LENGTH = 0.06
TIBIA_LENGTH = 0.06
LIMB_MASS = 0.067

def sphere_inertia(mass, radius):
    return (2. / 5) * mass * (radius **2)

SURFACE = '''
        <surface>
          <contact>
            <ode>
              <kp>100.0</kp>
              <kd>100.0</kd>
            </ode>
          </contact>
        </surface>
'''

PARAMETERS = {
    'chassis_mass' : CHASSIS_MASS,
    'chassis_inertia' : sphere_inertia(4 * CHASSIS_MASS, 0.5 * CHASSIS_LENGTH),
    'chassis_length' : CHASSIS_LENGTH,
    'chassis_height' : 0.034,
    'height' : 0.4,
    'surface' : '',
    'effort' : 1.2,
    }

PREAMBLE = '''<?xml version="1.0"?>
<sdf version="1.4">
  <model name="mj_mech">
    <static>false</static>

'''

SUFFIX = '''
  </model>
</sdf>
'''

CHASSIS = '''
    <link name="chassis">
      <pose>0 0 {height:f} 0 0 0</pose>
      <inertial>
        <mass>{chassis_mass:f}</mass>
        <inertia>
          <ixx>{chassis_inertia:f}</ixx>
          <ixy>0.00</ixy>
          <ixz>0.00</ixz>
          <iyy>{chassis_inertia:f}</iyy>
          <iyz>0.00</iyz>
          <izz>{chassis_inertia:f}</izz>
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry><box><size>{chassis_length:f} {chassis_length:f} {chassis_height:f}</size></box></geometry>
      </collision>
      <visual name="visual">
        <geometry><mesh><uri>file://chassis.dae</uri></mesh></geometry>
      </visual>
    </link>
'''


LINK = '''
    <link name="{name}">
      <pose>{x:f} {y:f} {z:f} {roll_rad:f} {pitch_rad:f} {yaw_rad:f}</pose>
      <inertial>
        <mass>{mass:f}</mass>
        <inertia>
          <ixx>{inertia:f}</ixx>
          <ixy>0.00</ixy>
          <ixz>0.00</ixz>
          <iyy>{inertia:f}</iyy>
          <iyz>0.00</iyz>
          <izz>{inertia:f}</izz>
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry><box><size>{length:f} {width:f} {height:f}</size></box></geometry>
      {surface}
      </collision>
      <visual name="visual">
        <geometry><box><size>{length:f} {width:f} {height:f}</size></box></geometry>
      </visual>
    </link>
'''

MESH_LINK = '''
    <link name="{name}">
      <pose>{x:f} {y:f} {z:f} {roll_rad:f} {pitch_rad:f} {yaw_rad:f}</pose>
      <inertial>
        <mass>{mass:f}</mass>
        <inertia>
          <ixx>{inertia:f}</ixx>
          <ixy>0.00</ixy>
          <ixz>0.00</ixz>
          <iyy>{inertia:f}</iyy>
          <iyz>0.00</iyz>
          <izz>{inertia:f}</izz>
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry><box><size>{length:f} {width:f} {height:f}</size></box></geometry>
      {surface}
      </collision>
      <visual name="visual">
        <geometry><mesh><uri>{mesh_name:s}</uri></mesh></geometry>
      </visual>
    </link>
'''

LIMIT = '''
        <limit>
          <effort>100</effort>
          <velocity>1.0</velocity>
        </limit>
'''

JOINT = '''
    <joint type="revolute" name="{name}">
      <pose>{x:f} {y:f} {z:f} 0 0 0</pose>
      <child>{child}</child>
      <parent>{parent}</parent>
      <axis>
        <xyz>{axis_x:f} {axis_y:f} {axis_z:f}</xyz>
        <dynamics><damping>0.1</damping><friction>0.1</friction></dynamics>
        <limit>
          <effort>{effort:f}</effort>
          <velocity>3.0</velocity>
        </limit>
      </axis>
    </joint>
'''

TIP = '''
    <link name="{name}">
      <pose>{x:f} {y:f} {z:f} 0 0 0</pose>
      <inertial>
        <mass>{mass:f}</mass>
        <inertia>
          <ixx>{inertia:f}</ixx>
          <ixy>0.00</ixy>
          <ixz>0.00</ixz>
          <iyy>{inertia:f}</iyy>
          <iyz>0.00</iyz>
          <izz>{inertia:f}</izz>
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry><sphere><radius>{radius:f}</radius></sphere></geometry>
        {surface}
      </collision>
      <visual name="visual">
        <geometry><empty/></geometry>
      </visual>
    </link>
'''

TIP_JOINT = '''
    <joint type="revolute" name="{name}">
      <pose>{x:f} {y:f} {z:f} 0 0 0</pose>
      <child>{child}</child>
      <parent>{parent}</parent>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <upper>0</upper>
          <lower>0</lower>
        </limit>
        <dynamics><damping>0.1</damping><friction>0.1</friction></dynamics>
      </axis>
    </joint>
'''



def merge(dict1, dict2):
    copy = dict1.copy()
    copy.update(dict2)
    return copy

def main():
    print PREAMBLE

    print CHASSIS.format(**PARAMETERS)

    print MESH_LINK.format(
        **merge(PARAMETERS,
                {'name' : 'pan_aeg',
                 'x' : 0.0,
                 'y' : 0.01,
                 'z' : PARAMETERS['height'] + PARAMETERS['chassis_height'] + 0.025,
                 'mass' : 0.1,
                 'inertia' : 10 * sphere_inertia(0.1, 0.02),
                 'pitch_rad' : 0,
                 'roll_rad' : 0,
                 'yaw_rad' : 0,
                 'width' : 0.04,
                 'length' : 0.02,
                 'height' : 0.025,
                 'mesh_name' : 'pan_bracket.dae'
                 }))

    print JOINT.format(
        **merge(PARAMETERS, {'name' : 'pan_aeg_hinge',
                             'x' : 0.0,
                             'y' : 0.0,
                             'z' : 0.0,
                             'child' : 'pan_aeg',
                             'parent' : 'chassis',
                             'axis_x' : 0.0,
                             'axis_y' : 0.0,
                             'axis_z' : 1.0,
                             }))

    print MESH_LINK.format(
        **merge(PARAMETERS,
                {'name' : 'weapon_assembly',
                 'x' : 0.0,
                 'y' : 0.01,
                 'z' : PARAMETERS['height'] + PARAMETERS['chassis_height'] + 0.047,
                 'mass' : 0.550,
                 'inertia' : 3 * sphere_inertia(0.55, 0.2),
                 'pitch_rad' : 0,
                 'roll_rad' : 0,
                 'yaw_rad' : 0,
                 'width' : 0.035,
                 'length' : 0.15,
                 'height' : 0.15,
                 'mesh_name' : 'weapon_assembly.dae'
                 }))

    print JOINT.format(
        **merge(PARAMETERS, {'name' : 'weapon_assembly_hinge',
                             'x' : 0.0,
                             'y' : 0.0,
                             'z' : 0.0,
                             'child' : 'weapon_assembly',
                             'parent' : 'pan_aeg',
                             'axis_x' : 1.0,
                             'axis_y' : 0.0,
                             'axis_z' : 0.0,
                             }))


    leg_x_sign = [ 1, 1, -1, -1]
    leg_y_sign = [ 1, -1, -1, 1]
    leg_yaw = [ 0, 0, math.pi, math.pi ]

    half_chassis_width = 0.5 * CHASSIS_LENGTH + 0.005
    half_chassis_length = 0.5 * CHASSIS_LENGTH - 0.014
    leg_z = 0.011

    for leg_num in range(4):

        print MESH_LINK.format(
            **merge(PARAMETERS,
                    {'name' : 'coxa%d' % leg_num,
                     'x' : leg_x_sign[leg_num] * half_chassis_width,
                     'y' : leg_y_sign[leg_num] * half_chassis_length,
                     'z' : PARAMETERS['height'] + leg_z,
                     'mass' : LIMB_MASS,
                     'inertia' : 10 * sphere_inertia(LIMB_MASS, 0.06),
                     'roll_rad' : 0,
                     'pitch_rad' : 0,
                     'yaw_rad' : leg_yaw[leg_num],
                     'length' : COXA_LENGTH,
                     'width' : 0.03,
                     'height' : 0.035,
                     'mesh_name' : 'file://coxa.dae'}))
        print JOINT.format(
            **merge(PARAMETERS, {'name' : 'coxa_hinge%d' % leg_num,
                                 'x' : 0.0,
                                 'y' : 0.0,
                                 'z' : 0.0,
                                 'child' : 'coxa%d' % leg_num,
                                 'parent' : 'chassis',
                                 'axis_x' : 0.0,
                                 'axis_y' : 0.0,
                                 'axis_z' : 1.0}))

        print MESH_LINK.format(
            **merge(PARAMETERS,
                    {'name' : 'femur%d' % leg_num,
                     'x' : leg_x_sign[leg_num] * (half_chassis_width + COXA_LENGTH),
                     'y' : leg_y_sign[leg_num] * half_chassis_length,
                     'z' : PARAMETERS['height'] + leg_z,
                     'mass' : LIMB_MASS,
                     'inertia' : 10 * sphere_inertia(LIMB_MASS, 0.06),
                     'roll_rad' : 0,
                     'pitch_rad' : 0,
                     'yaw_rad' : leg_yaw[leg_num],
                     'length' : FEMUR_LENGTH,
                     'width' : 0.035,
                     'height' : 0.030,
                     'mesh_name' : 'file://femur.dae'}))

        print JOINT.format(
            **merge(PARAMETERS,
                    {'name' : 'femur_hinge%d' % leg_num,
                     'x' : 0.0,
                     'y' : 0.0,
                     'z' : 0.0,
                     'child' : 'femur%d' % leg_num,
                     'parent' : 'coxa%d' % leg_num,
                     'axis_x' : 0.0,
                     'axis_y' : leg_x_sign[leg_num] * 1.0,
                     'axis_z' : 0.0}))

        print MESH_LINK.format(
            **merge(PARAMETERS,
                    {'name' : 'tibia%d' % leg_num,
                     'x' : leg_x_sign[leg_num] * (half_chassis_width + COXA_LENGTH + FEMUR_LENGTH),
                     'y' : leg_y_sign[leg_num] * half_chassis_length,
                     'z' : PARAMETERS['height'] + leg_z,
                     'mass' : LIMB_MASS,
                     'inertia' : 10 * sphere_inertia(LIMB_MASS, 0.06),
                     'roll_rad' : 0.0,
                     'pitch_rad' : 0.0,
                     'yaw_rad' : leg_yaw[leg_num],
                     'length' : TIBIA_LENGTH,
                     'width' : 0.035,
                     'height' : 0.030,
                     'mesh_name' : 'file://bracket_long_tip.dae'}))

        print JOINT.format(
            **merge(PARAMETERS,
                    {'name' : 'tibia_hinge%d' % leg_num,
                     'x' : 0.0,
                     'y' : 0.0,
                     'z' : 0.0,
                     'child' : 'tibia%d' % leg_num,
                     'parent' : 'femur%d' % leg_num,
                     'axis_x' : 0.0,
                     'axis_y' : leg_x_sign[leg_num] * 1.0,
                     'axis_z' : 0.0}))

        print TIP.format(
            **merge(PARAMETERS,
                    {'name' : 'tip%d' % leg_num,
                     'x' : leg_x_sign[leg_num] * (half_chassis_width + COXA_LENGTH + FEMUR_LENGTH + TIBIA_LENGTH),
                     'y' : leg_y_sign[leg_num] * (half_chassis_length),
                     'z' : PARAMETERS['height'] + leg_z,
                     'mass' : 0.02,
                     'inertia' : sphere_inertia(0.02, 0.017),
                     'radius' : 0.012}))

        print TIP_JOINT.format(
            **merge(PARAMETERS,
                    {'name' : 'tip_hinge%d' % leg_num,
                     'x' : 0.0,
                     'y' : 0.0,
                     'z' : 0.0,
                     'child' : 'tip%d' % leg_num,
                     'parent' : 'tibia%d' % leg_num,
                     }))


    print SUFFIX

if __name__ == '__main__':
    main()

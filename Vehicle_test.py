import unittest
import math
import pygame
import Simulation as sim
import GlobalData as GD
from Vehicle import VehicleClass
from unittest.mock import patch
import FileController as fc


class TestVehicleClass(unittest.TestCase):
    def setUp(self):
        GD.vehicles_generating  = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='generating_number')
        GD.vehicles_weight      = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='weight')
        GD.speeds               = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='speed')
        # Initialize Pygame
        pygame.init()

        # Set the display mode
        self.screen = pygame.display.set_mode((640, 480))
        self.vehicle = VehicleClass(
                lane            = GD.CD, 
                vehicle_class   =  "car", 
                direction       = GD.RIGHT, 
                will_turn_right = False, 
                will_turn_left  = False,
                x               = 0,
                y               = 0
                )
        pygame.display.flip()
        GD.vehicles_[GD.RIGHT][GD.CD].append(self.vehicle)
        # Set up a fake GD module with test data
        GD.circle_coordinates = {
            GD.RIGHT:{ #        # RIGHT
                GD.CD: 
                    {
                    'pos':(370,83),
                    'radius':45
                    }
           
            }
        }
        GD.circle_params_for_rotation = {
            GD.RIGHT:{         # RIGHT
                GD.CD:[0,-1, 1,-1],
                GD.KL:[0,-1, 1,-1],
                GD.ST:[0,-1, 1,-1],
                GD.WX:[0, 1,-1, 1]
              }
        }

        GD.rotate_point = {
            GD.RIGHT: {
                GD.CD: 50,
                GD.KL: 60,
                GD.ST: 70,
                GD.WX: 80
            }
        }
        GD.next_lane_of = {
            GD.RIGHT: {
                GD.CD: (GD.UP, GD.CD),
                GD.KL: (GD.UP, GD.KL),
                GD.ST: (GD.UP, GD.ST),
                GD.WX: (GD.UP, GD.WX)
            }
        }
        GD.vehicles_ = {
            GD.RIGHT: {
                GD.CD: [],
                GD.KL: [],
                GD.ST: [],
                GD.WX: []
            }
        }

    def test_init(self):
        # Test default values
        self.assertEqual(self.vehicle.lane, 0)
        self.assertEqual(self.vehicle.vehicle_class, "car")
        self.assertEqual(self.vehicle.speed, GD.speeds["car"])
        self.assertEqual(self.vehicle.direction, 'right')
        self.assertEqual(self.vehicle.x, 0)
        self.assertEqual(self.vehicle.y, 0)
        self.assertEqual(self.vehicle.crossed, 0)
        self.assertEqual(self.vehicle.will_turn_right, False)
        self.assertEqual(self.vehicle.will_turn_left, False)
        self.assertEqual(self.vehicle.turned, 0)
        self.assertEqual(self.vehicle.rotate_angle, 0)
        self.assertIsInstance(self.vehicle.image, pygame.rect.Rect)
        self.assertIsInstance(self.vehicle.all_sprites, pygame.sprite.Group)
        self.assertEqual(self.vehicle.speed_avg, 0)
        self.assertEqual(self.vehicle.Kilometre, 0)
        

    def test_apply_circle_rotation(self):
        # Test when rotate_angle is less than 88
        self.vehicle.rotate_angle = 87
        result = self.vehicle.apply_circle_rotation(self.screen)
        self.assertEqual(result, True)
        self.assertEqual(self.vehicle.rotate_angle, 88.9)
        self.assertIsInstance(self.vehicle.image, pygame.Surface)
        self.assertIsInstance(self.vehicle.rect, pygame.rect.Rect)

        # Test when rotate_angle is equal or bigger to 88
        self.vehicle.rotate_angle = 88
        result = self.vehicle.apply_circle_rotation(self.screen)
        self.assertEqual(result, False)
        self.assertEqual(self.vehicle.rotate_angle, 90)
  
    def test_move_right_cd_lane(self):
        # Test moving in right direction, CD lane
        # Set vehicle position and rotation angle
        self.vehicle.x = 45
        self.vehicle.rotate_angle = 0
        # Test moving without rotating
        self.vehicle.move_(self.screen)
        self.assertEqual(self.vehicle.x, 45)
        self.assertEqual(self.vehicle.rotate_angle, 0)
        # Test rotating and moving
        self.vehicle.x = 49
        self.vehicle.rotate_angle = 89
        self.vehicle.move_(self.screen)
        self.assertEqual(self.vehicle.x, 49)
        self.assertEqual(self.vehicle.rotate_angle, 89)
        self.assertEqual(self.vehicle.direction, GD.RIGHT)
        self.assertEqual(self.vehicle.lane, GD.CD)
        
        
if __name__ == '__main__':
    unittest.main()

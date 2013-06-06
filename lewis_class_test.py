#!/usr/bin/python
# Copyright 2012 Aaron S. Joyner <aaron@joyner.ws>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import lewis_class
import random
import unittest

class TestLewisClassScorer(unittest.TestCase):
  def test_simple(self):
    """Test the basic behavior of the sorting and dividing."""
    scores = [[7, 7], [9, 9], [4, 4], [8, 8], [6, 6], [1, 1], [3, 3], [5, 5],
              [2, 2]]
    grouped_scores = [[[9, 9], [8, 8], [7, 7]],  # Group 0
                      [[6, 6], [5, 5], [4, 4]],  # Group 1
                      [[3, 3], [2, 2], [1, 1]]]  # Group 2
    
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=3,
                                          scoring_fields=2)
    self.assertEqual(grouped_scores, output)

  def test_short_upper_class(self):
    """Test that the short class will be the upper class."""
    scores = [[7, 7], [9, 9], [4, 4], [8, 8], [6, 6], [1, 1], [3, 3], [5, 5]]
    grouped_scores = [[[9, 9], [8, 8]],  # Group 0
                      [[7, 7], [6, 6], [5, 5]],  # Group 1
                      [[4, 4], [3, 3], [1, 1]]]  # Group 2
    
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=3,
                                          scoring_fields=2)
    self.assertEqual(grouped_scores, output)

    scores = [[7, 7], [9, 9], [4, 4], [8, 8], [6, 6], [3, 3], [5, 5]]
    grouped_scores = [[[9, 9], [8, 8], [7, 7]],  # Group 0
                      [[6, 6], [5, 5], [4, 4], [3, 3]]]  # Group 1
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=2,
                                          scoring_fields=2)
    self.assertEqual(grouped_scores, output)

  def test_tie_uses_secondary(self):
    scores = [[0, 9, 'Aaron'],
              [0, 8, 'Brian'],
              [0, 7, 'Chuck'],
              [0, 6, 'Doris'],
              [0, 5, 'Elena'],
              [0, 4, 'Frank'],
              [0, 3, 'Gavin'],
              [0, 2, 'Hanna'],
              [0, 1, 'Irine']]
    grouped_scores = [[[0, 9, 'Aaron'],  # Group 1
                       [0, 8, 'Brian'],
                       [0, 7, 'Chuck']],
                      [[0, 6, 'Doris'],  # Group 2
                       [0, 5, 'Elena'],
                       [0, 4, 'Frank']],
                      [[0, 3, 'Gavin'],  # Group 3
                       [0, 2, 'Hanna'],
                       [0, 1, 'Irine']]]
    
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=3,
                                          scoring_fields=2)
    self.assertEqual(grouped_scores, output)

  def test_numerical_sorting(self):
    """Ensures that ints are sorted numerically not lexicaly."""
    scores = [[3], [20], [100]]
    grouped_scores = [[[100]], [[20]], [[3]]]
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=3,
                                          scoring_fields=1)
    self.assertEqual(grouped_scores, output)

  def test_group_boundary_shifts_up(self):
    scores = [[100, 'Jim'],
              [99, 'Jan'],
              [99, 'John'],
              [98, 'Terry'],
              [96, 'Eric'],
              [96, 'Susie'],
              [95, 'Dolly'],
              [95, 'Mike'],
              [94, 'Sam'],
              [94, 'Dana'],
              [93, 'Joshua'],
              [93, 'Janie'],
              [93, 'Debbie'],
              [92, 'Lucy'],
              [92, 'Patty'],
              [91, 'Zelda'],
              [91, 'George'],
              [90, 'Paul'],
              [90, 'Rita'],
              [90, 'Ofelia'],
              [90, 'Pamela'],
              [89, 'Greg'],
              [89, 'Art'],
              [88, 'Olga'],
              [85, 'Joseph'],
              [85, 'Mary'],
              [84, 'Will'],
              [80, 'Lee'],
              [79, 'Renee'],
              [75, 'Jonathon'],
              [74, 'Lisa'],
              [70, 'Bart']]
    grouped_scores = [[[100, 'Jim'],
                       [99, 'John'],
                       [99, 'Jan'],
                       [98, 'Terry'],
                       [96, 'Susie'],
                       [96, 'Eric']],

                      [[95, 'Mike'],
                       [95, 'Dolly'],
                       [94, 'Sam'],
                       [94, 'Dana'],
                       [93, 'Joshua'],
                       [93, 'Janie'],
                       [93, 'Debbie']],

                      [[92, 'Patty'],
                       [92, 'Lucy'],
                       [91, 'Zelda'],
                       [91, 'George']],

                      [[90, 'Rita'],
                       [90, 'Paul'],
                       [90, 'Pamela'],
                       [90, 'Ofelia'],
                       [89, 'Greg'],
                       [89, 'Art'],
                       [88, 'Olga']],

                      [[85, 'Mary'],
                       [85, 'Joseph'],
                       [84, 'Will'],
                       [80, 'Lee'],
                       [79, 'Renee'],
                       [75, 'Jonathon'],
                       [74, 'Lisa'],
                       [70, 'Bart']]]
    
    
    self.maxDiff = None
    random.shuffle(scores)
    output = lewis_class.LewisClassScorer(scores, num_classes=5,
                                          scoring_fields=1)
    self.assertEqual(grouped_scores, output)


if __name__ == '__main__':
  unittest.main()


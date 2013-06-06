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

"""Lewis Class Scorer for calculating multiple classes of winners of an event.

This is based on the National Sporting Clays Association PDF on Lewis Class
Scoring, included with this distribution or available here: http://goo.gl/Ys0IK

There are two basic ways to use this code, as a script, or as a module.

Example usage as a stand-alone script:
- Create a file with scores, with your scoring criteria as space-separated
  items, from most to least important.  This example uses sporting clays
  scores, and shots before first miss to break ties.
  Note: You do not have to sort the input.

42 4 Tim Miller
47 21 Tim Brooks
35 6 Aaron Joyner

- Invoke this script and pass the path to that file as an argument:
./lewis_class.py ./path/to/scores
- It will print something like this:
Group 0
  47 21 Tim Brooks
  46 06 Bob Fleming
  46 04 Linc Huffman
Group 1
  37 02 Ken Callahan
  36 03 David Carswell
  36 00 Ivan Livas
Group 2
  25 00 Aaron Carswell
  24 01 Sasha Glenn
  24 01 Michael Callahan

Example usage as a module:
import lewis_class
scores = [[42, 2, 'Tim Miller'],
          [47, 21, 'Tim Brooks'],
          [35, 6, 'Aaron Joyner']]
classes = lewis_class.LewisClassScorer(scores)
"""

import argparse
import sys
from operator import itemgetter, attrgetter


def LewisClassScorer(scores, num_classes=3, scoring_fields=1):
  """Score and divide into groups a list, as per Lewis Class rules.
  
  Args:
    scores: a list of lists, which will be sorted in descending order.  The
            first element of each list must be a number.  The elements must be
            sortable (See the module doc string for an example).
            Tip: You probably want int not string scoring_fields, so they sort
                 numerically instead of lexically.
    num_classes: The number of classes that the scores should be divided into.
    scoring_fields: The number of fields that are relevant to the score.  This
                    allows you to supply the last field as a "Name", and have
                    it ignored for evaluating ties.  If None, all fields are
                    relevant, onlye exact duplicates are considered ties.

  Returns:
    A list of length num_classes, where each element is a list from the list of
    "scores" provided, ranked as per Lewis Class Scoring.  eg:
    [[winner, runnerup], [2ndwinner, 2ndrunnerup], [3rdwinner, 3rup1, 3rup2]]
  """
  # Sort the incoming entries by score, then longest run
  scores.sort(reverse=True)

  num_scores = len(scores)
  base_class_size = num_scores / num_classes
  remainder = num_scores % num_classes

  #print "base_class_size: %s" % base_class_size
  #print "remainder: %s" % remainder
  breakpoints = []
  for i in xrange(0, num_classes):
    size = (i * base_class_size)
    if i > num_classes - remainder:
      size += 1
    breakpoints.append(size)
  #print "Breaks at positions: %s" % breakpoints

  # Get the score at each break point
  class_winning_score = []
  for i in breakpoints:
    class_winning_score.append(scores[i][0])
  #print "Each class' unajusted winning score: %s" % groups_winning_score

  # Adjust the breakpoint by shifting scores around the line
  for class_number, bp in enumerate(breakpoints):
    if class_number == 0: continue  # skip the highest class, it can't adjust

    # Determine how many above and below had the same score
    breakpoint_score = scores[bp][0:scoring_fields]
    equal_scores_above = 0
    for offset in xrange(1, num_scores):  # the line is 'above' the breakpoint
      if scores[bp - offset][0:scoring_fields] == breakpoint_score:
        equal_scores_above += 1
      else:
        break
    equal_scores_below = 0
    for offset in xrange(0, num_scores):  # the line is 'above' the breakpoint
      if (bp + offset) >= num_scores:
        break
      if scores[bp + offset][0:scoring_fields] == breakpoint_score:
        equal_scores_below += 1
      else:
        break

    if equal_scores_above == equal_scores_below:
      if equal_scores_above == 0:
        continue # no tie at the break line
      breakpoints[class_number] = bp - equal_scores_above

    if equal_scores_above > equal_scores_below:
      # If there are more scores above, move the break point past the current
      # position, and past any equal_scores_below
      breakpoints[class_number] = bp + equal_scores_below
    
    if equal_scores_above < equal_scores_below:
      # if there are more scores below, back the break point up above them
      breakpoints[class_number] = bp - equal_scores_above

  #print "Adjusted breaks at positions: %s" % breakpoints

  # Return the classes as a list of lists [[score1, ...], [score3]..]
  classes = []
  for class_number, bp in enumerate(breakpoints):
    try:
      classes.append(scores[bp:breakpoints[class_number+1]])
    except IndexError:
      classes.append(scores[bp:])  # breakpoints isn't terminated...
  return classes


def main(argv):
  parser = argparse.ArgumentParser(
      description='Score winners of multiple classes in an event.')
  parser.add_argument('-c', '--num_classes', default=3, type=int,
      help='The number of classes to divide the participants into.')
  parser.add_argument('-w', '--num_winners', default=3, type=int,
      help='The number of winners to print in each class.')
  parser.add_argument('-f', '--scoring_fields', default=2, type=int,
      help=('The number of space-separated fields in the input file to '
            'consider as part of the score.'))
  parser.add_argument('-a', '--print_all', action='store_true',
      help='Print the entirety of each class, not just the winners.')
  parser.add_argument('filename', type=file)
  args = parser.parse_args()

  if len(argv) < 2:
    print "Please specify a filename."
    sys.exit(1)
  scores = []
  for linenum, line in enumerate(args.filename):
    line = line.rstrip()
    if len(line) == 0 or line.startswith('#'):
      continue
    score = line.split(' ')
    for i in xrange(0, args.scoring_fields):
      try:
        score[i] = int(score[i])
      except (IndexError, ValueError), e:
        print 'Unable to parse line %d: %s' % (linenum, e)
        print 'Did you specify to large a --scoring_fields?'
        sys.exit(1)
    scores.append(score)

  classes = LewisClassScorer(scores,
                             num_classes=args.num_classes,
                             scoring_fields=args.scoring_fields)

  if args.print_all:
    args.num_winners = sys.maxint

  # pretty print the num_winners in each class
  for class_number, scores in enumerate(classes):
    print "Class %s" % (class_number + 1)
    for score in scores[0:args.num_winners]:
      print "  %s" % ' '.join(str(x) for x in score)


if __name__ == '__main__':
  main(sys.argv)

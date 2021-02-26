# 2021 <3
# Let's go boyz

from os import name
from typing import List, Tuple
import sys
import math
import numpy as np


class Intersection:

  def __init__(self, id: int):
    """
    id - id integer
    incommingStreets - list of streets that start here
    outcommingStreets - list of streets that end here
    """

    self.id = id
    self.incomingStreets = []
    self.outcomingStreets = []
    self.score = 0
    self.schedule = None


class Schedule:

  def __init__(self, intersection: Intersection):
    self.intersection = intersection
    # [(0, incStreet) for incStreet in intersection.incommingStreets)]
    self.times = None
    # self.scheduleTime = 0


class Street:

  def __init__(self, name: str, start: Intersection, end: Intersection, time: int):
    """
    name - name string
    start - Intersection start
    end - Intersection end
    time - time that it takes to cross the street
    """

    self.name = name
    self.start = start
    self.end = end
    self.time = time
    self.cars = 0
    self.score = 0
    # self.score = 0

  def initIntersections(self):
    self.start.outcomingStreets.append(self)
    self.end.incomingStreets.append(self)

    self.end.score += self.cars
    # TODO: not all cars pass the end score


class Car:

  def __init__(self, id, path: List[Street]):
    """
    id - id integer
    path - list of streeds that car needs to cross
    """

    self.id = id
    self.path = path
    self.totalTime = 0
    # self.order = order

    # add car to street
    for street in path:
      street.cars += 1
      self.totalTime += street.time
    for street in path:
      street.score += len(self.path)


def getStreet(streetName: str, streets: List[Street]):
  for street in streets:
    if street.name == streetName:
      return street
  raise ValueError('No street found in the Street list')


def getIntersection(intersectionId: int, intersections: List[Intersection]):
  for intersection in intersections:
    if intersection.id == intersectionId:
      return intersection
  raise ValueError('No intersection found in the Intersection list')


def parse(fileName):
  print('Parser started...')
  file = open(fileName, 'r')

  # first line
  duration, intersectionCount, streetCount, carCount, F = tuple(
      map(int, file.readline().strip().split()))

  print('Parser: creating intersections...')
  # create intersections
  intersections = [Intersection(i) for i in range(intersectionCount)]

  print('Parser: reading streets...')
  # reading intersection
  streets = {}
  for i in range(streetCount):
    startIntersection, endIntersection, name, time = file.readline().strip().split()
    streets[name] = Street(name, intersections[int(
        startIntersection)], intersections[int(endIntersection)], int(time))

  print('Parser: reading paths')
  # reading car paths
  cars = []
  for i in range(carCount):
    carStreets = [streets[name]
                  for name in file.readline().strip().split()[1:]]
    cars.append(Car(i, carStreets))

  print('Parser: filtering streets...')
  # filter unused streets
  # streets = list(filter(lambda key: streets[key].cars > 0, streets))
  streetsX = {}
  for key in streets:
    if streets[key].cars > 0:
      streetsX[key] = streets[key]
  streets = streetsX

  print('Parser: scoring intersections')
  # generate score for intersections
  for key in streets:
    streets[key].initIntersections()

  print('Parser: filtering intersections...')
  # filter unused intersections
  intersections = list(filter(lambda x: x.score > 0, intersections))

  print('Parser: Creating schedules')
  for intersection in intersections:
    intersection.schedule = Schedule(intersection)

  file.close()
  print('Parser ended')
  return duration, carCount, F, streets, cars, intersections


def output(fileName: str, schedules: List[Schedule]):
  print('Output serializer started...')
  outFile = open(fileName, 'w')
  outFile.write(str(len(schedules)) + '\n')
  for schedule in schedules:
    outFile.write(str(schedule.intersection.id) + '\n')
    outFile.write(str(len(schedule.times)) + '\n')
    for st in schedule.times:
      outFile.write(st[1].name + " " + str(st[0]) + '\n')
  outFile.close()
  print('Output serializer ended...')


def sortKey():
  pass


# Process all the files
fileNames = ['A.txt', 'B.txt', 'C.txt', 'D.txt', 'E.txt', 'F.txt']

# parse
duration, carCount, F, streets, cars, intersections = parse(sys.argv[1])

# Generate a schedule for each intersections
# schedules: List[Tuple[Intersection, List[Tuple[int, Street]]]] = []
for intersection in intersections:
  gcd = np.gcd.reduce([incSt.cars for incSt in intersection.incomingStreets])
  # gcd = 10
  intersection.schedule.times = [math.floor((min(incStr.cars // gcd, duration)//10), incStr)
                                 for incStr in intersection.incomingStreets]
  intersection.schedule.times.sort(key=lambda x: x[0], reverse=True)

output(sys.argv[1] + '.out', list(map(lambda x: x.schedule, intersections)))

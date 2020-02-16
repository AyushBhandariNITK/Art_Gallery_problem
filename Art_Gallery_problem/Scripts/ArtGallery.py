
"""
description: Art Gallery Pedagogical Tool
Provides functionality to solve the Art Gallery problem
using Triangulation and Edge Detection
"""

import pygame, sys
from pygame import gfxdraw
import mcoloring
import PolygonVisibility
from pygame.locals import *
import polytri
import easygui

def _intersection(P1, P2, P3):
    """
    Intersection support function
    :param P1: point 1
    :param P2: point 2
    :param P3: point 3
    :return:
    """
    return (P3[1] - P1[1]) * (P2[0] - P1[0]) > (P2[1] - P1[1]) * (P3[0] - P1[0])

def findIntersection(S1x, S1y, D1x, D1y, S2x, S2y, D2x, D2y):
    """
    Find if 2 line segments intersect
    :param S1x: x coordinate of segment 1's start point
    :param S1y: y coordinate of segment 1's start point
    :param D1x: x coordinate of segment 1's end point
    :param D1y: y coordinate of segment 1's end point
    :param S2x: x coordinate of segment 2's start point
    :param S2y: y coordinate of segment 2's start point
    :param D2x: x coordinate of segment 2's end point
    :param D2y: y coordinate of segment 2's end point
    :return: Intersection point [x,y]
    """
    return _intersection([S1x,S1y],[S2x,S2y],[D2x,D2y]) != _intersection([D1x,D1y],[S2x,S2y],[D2x,D2y]) and _intersection([S1x,S1y],[D1x,D1y],[S2x,S2y]) != _intersection([S1x,S1y],[D1x,D1y],[D2x,D2y])

def displayStatus(statusMsg):
    """
    Function to display the current status of the tool
    :param statusMsg: Status Message
    :return:
    """
    gfxdraw.filled_polygon(screen, [[0, 0], [0, 24], [WINDOW_WIDTH, 24], [WINDOW_WIDTH, 0]], WHITE)
    status = myfont.render(
        statusMsg, 1,
        BLACK)
    screen.blit(status, (10, 10))


def displayLabel1(labelMsg):
    """
    Function to display the options label line 1
    :param labelMsg: options string
    :return:
    """
    gfxdraw.filled_polygon(screen,
                           [[0, WINDOW_HEIGHT - 30], [0, WINDOW_HEIGHT - 16], [WINDOW_WIDTH, WINDOW_HEIGHT - 16],
                            [WINDOW_WIDTH, WINDOW_HEIGHT - 30]], WHITE)
    label1 = myfont.render(
        labelMsg, 1,
        BLACK)
    screen.blit(label1, (10, WINDOW_HEIGHT - 30))


def displayLabel2(labelMsg):
    """
    Function to display the options label line 2
    :param labelMsg: options string
    :return:
    """
    gfxdraw.filled_polygon(screen, [[0, WINDOW_HEIGHT - 15], [0, WINDOW_HEIGHT], [WINDOW_WIDTH, WINDOW_HEIGHT],
                                    [WINDOW_WIDTH, WINDOW_HEIGHT - 15]], WHITE)
    label2 = myfont.render(
        labelMsg, 1,
        BLACK)
    screen.blit(label2, (10, WINDOW_HEIGHT - 15))


def drawPolygon():
    """
    Function to draw the polygon
    :return:
    """
    pygame.font.init()
    myfont2 = pygame.font.SysFont('Comic Sans MS', 10)

    for i in range(len(points) - 1):
        pygame.draw.aaline(screen, BLUE, points[i], points[i + 1])
        textsurface = myfont2.render(str(i), False, (0, 0, 0))
        screen.blit(textsurface, (points[i][0], points[i][1]))
    textsurface = myfont2.render(str(len(points) - 1), False, (0, 0, 0))
    screen.blit(textsurface, (points[len(points) - 1][0], points[len(points) - 1][1]))
    pygame.draw.aaline(screen, BLUE, points[len(points) - 1], points[0])


def displayVariation(variation, guard):
    """
    Display a variation of the Art gallery problem and the visibility of the specified guard
    :param variation: the variation to be displayed
    :param guard: 0 for showing no guard's visibility or guard's id
    :return:
    """
    screen.fill(WHITE)

    displayLabel1("Switch between Variations (LEFT or RIGHT), Switch guard visibility (UP or DOWN),")
    displayLabel2("Reset (BACKSPACE)")
    displayStatus("The no. of guards sufficient to guard the gallery are " + str(
        len(variation)) + ". Displaying Variation " + str(currVariationDisplayed + 1) + " out of " + str(
        len(validColors)))

    pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
    pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))
    drawPolygon()
    if guard == 0:
        for p in variation:
            pygame.draw.circle(screen, rgb[validColors[currVariationDisplayed]], p[1], 5)
    if guard != 0:
        displayStatus("Loading...")
        pygame.display.update()
        visibility = PolygonVisibility.computeVisibility(points, variation[guard - 1][1])
        gfxdraw.filled_polygon(screen, visibility, BLUE)
        pygame.draw.circle(screen, BLACK, variation[guard - 1][1], 5)

        displayStatus("Visibility for variation " + str(currVariationDisplayed + 1) + "'s guard no. " + str(
            guard) + " out of " + str(len(variation)))


def process():
    """
    Process the Algorithm (Edge clipping & 3 - coloring)
    :return:
    """
    # print(points)
    gen = polytri.triangulate_poly(pts)
    adj_matrix = [[0 for __ in range(count)] for _ in range(count)]

    for x in gen:
        triangles.append(x[0])
        ears.append(x[1])
        x = x[0]
        adj_matrix[x[0][2]][x[1][2]] = 1
        adj_matrix[x[1][2]][x[0][2]] = 1
        adj_matrix[x[2][2]][x[1][2]] = 1
        adj_matrix[x[1][2]][x[2][2]] = 1
        adj_matrix[x[2][2]][x[0][2]] = 1
        adj_matrix[x[0][2]][x[2][2]] = 1

    g = mcoloring.Graph(count)
    g.graph = adj_matrix
    m = 3
    coloring = g.graphColouring(m)

    i = 0
    rgbCount = [0, 0, 0]
    for c in coloring:
        coloring3.append(c)
        rgbCount[c - 1] += 1
        variations[c - 1].append([i, pts[i][:2]])
        i += 1
    rgbMin = min(rgbCount)
    for i in range(len(rgbCount)):
        if rgbCount[i] == rgbMin:
            validColors.append(i)
    currVariationDisplayed = 0
    guardSelected = 0


def displayNext(i):
    """
    Display next step
    :param i: step number to be displayed
    :return:
    """
    if i < len(triangles):
        gfxdraw.filled_polygon(screen, [triangles[i][0][:2], triangles[i][1][:2], triangles[i][2][:2]], RED)
        pygame.draw.polygon(screen, BLUE, [triangles[i][0][:2], triangles[i][1][:2], triangles[i][2][:2]], 1)
        pygame.draw.circle(screen, GREEN, ears[i][:2], 8)


def displayPrev(index, mode):
    """
    Display previous step
    :param index: step number to be displayed
    :param mode: 0 for triangulation steps, 1 for 3 coloring steps
    :return:
    """
    indexTri = index
    if mode == 1:
        indexTri = len(triangles) - 1

    if mode == 0:
        screen.fill(WHITE)

        displayLabel1("Next step (RIGHT), Previous step (LEFT),")
        displayLabel2("Reset (BACKSPACE)")
        displayStatus("Running Ear-clipping Triangulation algorithm")
        pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
        pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))
        drawPolygon()

        i = -1
        while i < indexTri:
            i += 1
            displayNext(i)
            pygame.display.update()

    if mode == 1:
        displayTriangulated()
        i = -1
        displayStatus("Running 3-coloring algorithm")
        displayLabel1("Next step (RIGHT), Previous step (LEFT),")
        displayLabel2("Reset (BACKSPACE)")
        while i < index:
            i += 1
            display3Colors(i)
            pygame.display.update()


def displayTriangulated():
    """
    Display Triangulated Polygon
    :return:
    """
    screen.fill(WHITE)
    displayStatus("Displaying Triangulated Polygon")
    displayLabel1("Next step (RIGHT), Previous step (LEFT),")
    displayLabel2("Reset (BACKSPACE)")
    pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
    pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))

    for tri in triangles:
        if [tri[0][0], tri[0][1]] not in triPts:
            triPts.append([tri[0][0], tri[0][1]])
        if [tri[1][0], tri[1][1]] not in triPts:
            triPts.append([tri[1][0], tri[1][1]])
        if [tri[2][0], tri[2][1]] not in triPts:
            triPts.append([tri[2][0], tri[2][1]])
        pygame.draw.polygon(screen, BLUE, [tri[0][:2], tri[1][:2], tri[2][:2]], 1)


def display3Colors(i):
    """
    Display 3 coloring step
    :param i: step number
    :return:
    """
    index = -1
    for pt in points:
        index += 1
        if triPts[i] == pt[:2]:
            break
    pygame.draw.circle(screen, rgb[coloring3[index] - 1], triPts[i], 5)

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

rgb = [RED, GREEN, BLUE]

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 512

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('art gallery problem')
screen.fill(WHITE)
myfont = pygame.font.SysFont("Lucida Console", 12)
label1 = myfont.render(
    "Place first point (LEFT-MOUSE-CLICK), Load Polygon from file (SPACE)", 1,
    BLACK)
screen.blit(label1, (10, WINDOW_HEIGHT - 30))
label2 = myfont.render(
    "", 1,
    BLACK)
screen.blit(label2, (10, WINDOW_HEIGHT - 15))

status = myfont.render(
    "Start by building a polygon or loading a polygon from a file", 1,
    BLACK)
screen.blit(status, (10, 10))
pygame.draw.aaline(screen, BLACK, (0,25), (WINDOW_WIDTH,25))
pygame.draw.aaline(screen, BLACK, (0,WINDOW_HEIGHT-33), (WINDOW_WIDTH,WINDOW_HEIGHT-33))
clock = pygame.time.Clock()


lock = 0
pts = []
points=[]
mouse_lock = True
count = 0

variations=[[],[],[]]
validColors=[]
currVariationDisplayed = 0
guardSelected = 0
processed = 0
finished = 0
stepsFinish = 0
triangles = []
ears = []
triI = -1
coloring3 = []
colI = -1
triPts = []

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_SPACE] and lock!=1:
            path = easygui.fileopenbox()
            intersection = False
            with open(path) as dataFile:
                for line in dataFile:
                    lineSplit = line.split(" ")
                    currPt = [int(lineSplit[0]), int(lineSplit[1])]
                    for i in range(len(pts) - 2):
                        if findIntersection(currPt[0], currPt[1], pts[len(pts) - 1][0], pts[len(pts) - 1][1], pts[i][0], pts[i][1],
                                            pts[i + 1][0], pts[i + 1][1]):
                            intersection = True
                            break
                    if not intersection:
                        pt = [currPt[0], currPt[1], count]
                        count += 1
                        pts.append(pt)
                        points.append(pt[:2])
                        pygame.draw.circle(screen, BLACK, currPt, 3)
                        pygame.font.init()
                        myfont2 = pygame.font.SysFont('Comic Sans MS', 10)
                        textsurface = myfont2.render(str(count - 1), False, (0, 0, 0))
                        screen.blit(textsurface, (currPt[0], currPt[1]))
                        if len(pts) > 1:
                            pygame.draw.aaline(screen, BLUE, pts[len(pts) - 2][:2], currPt)
                    else:
                        break

                displayLabel1("Run (ENTER), Run step-by-step automatically (SPACE), Run step-by-step manually (RIGHT),")
                displayLabel2("Reset (BACKSPACE)")
                displayStatus("Choose an option to run the Algorithm")
                if not intersection:
                    for i in range(1, len(pts) - 2):
                        if findIntersection(pts[len(pts) - 1][0], pts[len(pts) - 1][1], pts[0][0], pts[0][1], pts[i][0],
                                            pts[i][1],
                                            pts[i + 1][0], pts[i + 1][1]):
                            intersection = True
                            break

                if not intersection:
                    pygame.draw.aaline(screen, BLUE, pts[len(pts) - 1][:2], pts[0][:2])
                    lock = 1
                else:
                    screen.fill(WHITE)

                    lock = 0
                    pts = []
                    points = []
                    count = 0

                    variations = [[], [], []]
                    validColors = []
                    currVariationDisplayed = 0
                    guardSelected = 0
                    processed = 0
                    finished = 0
                    stepsFinish = 0
                    triangles = []
                    ears = []
                    triI = -1
                    coloring3 = []
                    colI = -1
                    triPts = []

                    pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
                    pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))
                    displayLabel1("Place first point (LEFT-MOUSE-CLICK), Load Polygon from file (SPACE),")
                    displayLabel2("Reset (BACKSPACE)")
                    displayStatus(
                        "Cannot create simple polygon. Vertex " + str(currPt) + " doesn't produce a simple polygon.")

        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and lock != 1:
            displayLabel1("Finish Polygon (ENTER),")
            displayLabel2("Reset (BACKSPACE)")
            displayStatus("Continue adding vertices of the polygon, or press 'ENTER' to complete the Polygon")

            mpos = pygame.mouse.get_pos()
            intersection = False
            for i in range(len(pts)-2):
                if findIntersection(mpos[0],mpos[1],pts[len(pts)-1][0],pts[len(pts)-1][1],pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]):
                    intersection=True
                    break
            if not intersection:
                pt=[mpos[0],mpos[1],count]
                count+=1
                pts.append(pt)
                points.append(pt[:2])
                pygame.draw.circle(screen, BLACK, mpos, 3)
                pygame.font.init()
                myfont2 = pygame.font.SysFont('Comic Sans MS', 10)
                textsurface = myfont2.render(str(count-1), False, (0, 0, 0))
                screen.blit(textsurface, (mpos[0], mpos[1]))
                if len(pts) > 1:
                    pygame.draw.aaline(screen, BLUE, pts[len(pts) - 2][:2], mpos)
            else:
                displayStatus("Cannot insert this vertex as it doesn't produce a simple polygon. Please try again.")

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_RETURN] and lock == 1:
            process()
            processed = 1
            stepsFinish = 1
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)


        if event.type == KEYDOWN and pygame.key.get_pressed()[K_RETURN] and lock != 1 and len(pts) > 2:
            displayLabel1("Run (ENTER), Run step-by-step automatically (SPACE), Run step-by-step manually (RIGHT),")
            displayLabel2("Reset (BACKSPACE)")
            displayStatus("Choose an option to run the Algorithm")
            intersection = False
            for i in range(1,len(pts) - 2):
                if findIntersection(pts[len(pts)-1][0], pts[len(pts)-1][1], pts[0][0], pts[0][1], pts[i][0], pts[i][1],
                                    pts[i + 1][0], pts[i + 1][1]):
                    intersection = True
                    break

            if not intersection:
                pygame.draw.aaline(screen, BLUE, pts[len(pts)-1][:2], pts[0][:2])
                lock = 1
            else:
                displayStatus("Cannot insert this vertex as it doesn't produce a simple polygon. Please try again.")

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_SPACE] and lock == 1:
            process()
            processed = 1
            displayLabel1("Next step (RIGHT), Previous step (LEFT),")
            displayLabel2("Reset (BACKSPACE)")
            displayStatus("Running Ear-clipping Triangulation algorithm")
            while triI<len(triangles)-1:
                triI+=1
                displayNext(triI)
                pygame.display.update()
                pygame.time.delay(1000)
            displayStatus("Displaying Triangulated Polygon")
            displayTriangulated()
            pygame.display.update()
            pygame.time.delay(1000)
            displayStatus("Running 3-coloring algorithm")
            while colI < len(points)-1:
                colI += 1
                display3Colors(colI)
                pygame.display.update()
                pygame.time.delay(1000)
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)
            stepsFinish = 1

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_RIGHT] and lock == 1 and stepsFinish == 1:
            currVariationDisplayed = (currVariationDisplayed + 1)% len(validColors)
            guardSelected = 0
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_LEFT] and lock == 1 and stepsFinish == 1:
            currVariationDisplayed = (currVariationDisplayed - 1)% len(validColors)
            guardSelected = 0
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_LEFT] and lock == 1 and stepsFinish == 0:

            if triI == len(triangles) and colI>0 and colI<len(points):
                displayStatus("Running 3-coloring algorithm")
                displayLabel1("Next step (RIGHT), Previous step (LEFT),")
                displayLabel2("Reset (BACKSPACE)")
                colI -= 1
                displayPrev(colI, 1)
            elif triI == len(triangles) and colI==0:
                colI = -1
                displayTriangulated()
            elif triI<=len(triangles) and triI>0:
                displayStatus("Running Ear-clipping Triangulation algorithm")
                displayLabel1("Next step (RIGHT), Previous step (LEFT),")
                displayLabel2("Reset (BACKSPACE)")
                triI-=1
                displayPrev(triI, 0)
            elif triI==0:
                triI-=1
                screen.fill(WHITE)
                displayStatus("Displaying Original Polygon")
                displayLabel1("Previous step (LEFT),")
                displayLabel2("Reset (BACKSPACE)")

                pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
                pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))
                drawPolygon()

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_RIGHT] and lock == 1 and stepsFinish == 0:
            if processed != 1:
                process()
                processed = 1

            if triI<len(triangles)-1:
                displayStatus("Running Ear-clipping Triangulation algorithm")
                displayLabel1("Next step (RIGHT), Previous step (LEFT),")
                displayLabel2("Reset (BACKSPACE)")
                triI+=1
                displayNext(triI)
            elif triI == len(triangles)-1:

                triI+=1
                displayTriangulated()
            else:
                if colI<len(points)-1:
                    displayStatus("Running 3-coloring algorithm")
                    displayLabel1("Next step (RIGHT), Previous step (LEFT),")
                    displayLabel2("Reset (BACKSPACE)")
                    colI += 1
                    display3Colors(colI)
                elif colI==len(points)-1:
                    colI+=1
                    stepsFinish = 1
                    displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)



        if event.type == KEYDOWN and pygame.key.get_pressed()[K_UP] and lock == 1 and stepsFinish==1:
            guardSelected = (guardSelected-1)%(len(variations[validColors[currVariationDisplayed]])+1)
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_DOWN] and lock == 1 and stepsFinish==1:
            guardSelected = (guardSelected+1)%(len(variations[validColors[currVariationDisplayed]])+1)
            displayVariation(variations[validColors[currVariationDisplayed]], guardSelected)

        if event.type == KEYDOWN and pygame.key.get_pressed()[K_BACKSPACE]:
            screen.fill(WHITE)

            lock = 0
            pts = []
            points = []
            count = 0

            variations = [[], [], []]
            validColors = []
            currVariationDisplayed = 0
            guardSelected = 0
            processed = 0
            finished = 0
            stepsFinish = 0
            triangles = []
            ears = []
            triI = -1
            coloring3 = []
            colI = -1
            triPts = []

            pygame.draw.aaline(screen, BLACK, (0, 25), (WINDOW_WIDTH, 25))
            pygame.draw.aaline(screen, BLACK, (0, WINDOW_HEIGHT - 33), (WINDOW_WIDTH, WINDOW_HEIGHT - 33))

            displayStatus("Start by building a polygon or loading a polygon from a file")
            displayLabel1("Place first point (LEFT-MOUSE-CLICK), Load Polygon from file (SPACE)")
    pygame.display.update()
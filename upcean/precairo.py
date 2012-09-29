#!/usr/bin/python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2012 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2012 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2012 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: validate.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

import cairo;

'''
http://stevehanov.ca/blog/index.php?id=28
'''
def snapCoords( ctx, x, y ):
    (xd, yd) = ctx.user_to_device(x, y);
    return ( round(x) + 0.5, round(y) + 0.5 );

def drawLine( ctx, x1, y1, x2, y2 ):    
    point1 = snapCoords( ctx, x1, y1 );
    point2 = snapCoords( ctx, x2, y2 );
    ctx.move_to( point1[0], point1[1] );
    ctx.line_to( point2[0], point2[1] );
    ctx.set_line_width( 1.0 );
    ctx.stroke();

def drawColorLine( ctx, x1, y1, x2, y2, color ):
    ctx.set_source_rgb(color[0], color[1], color[2]);
    drawLine(ctx, x1, y1, x2, y2);
    ctx.close_path();
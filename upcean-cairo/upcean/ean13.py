'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: ean13.py - Last Update: 08/12/2013 Ver. 2.4.4 RC 2 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import cairo, re, sys, types, upcean.precairo, upcean.validate, upcean.convert;
import upcean.ean2, upcean.ean5;
from upcean.precairo import *;
from upcean.validate import *;
from upcean.convert import *;
from upcean.ean2 import *;
from upcean.ean5 import *;

def create_ean13(upc,outfile="./ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==8): 
  upc = convert_upce_to_ean13(upc);
 if(len(upc)==12): 
  upc = convert_upca_to_ean13(upc);
 if(len(upc)==12 and validate_upca(upc)==True): 
  upc = "0"+upc;
 if(len(upc)==12 and validate_upca(upc)==False): 
  upc = upc+str(validate_ean13(upc,true));
 if(len(upc)>13 or len(upc)<13): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(validate_ean13(upc)==False): 
  pre_matches = re.findall("^(\d{12})", upc); 
  upc = pre_matches[0]+str(validate_ean13(pre_matches[0],True));
 upc_matches = re.findall("(\d{1})(\d{6})(\d{6})", upc);
 if(len(upc_matches)<=0): 
  return False;
 upc_matches = upc_matches[0];
 PrefixDigit = upc_matches[0];
 LeftDigit = list(upc_matches[1]);
 RightDigit = list(upc_matches[2]);
 addonsize = 0;
 if(supplement!=None and len(supplement)==2): 
  addonsize = 29;
 if(supplement!=None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 115 + addonsize, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 115 + addonsize, barheight[1] + 8);
 upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
 upc_img.fill();
 if(hidetext==False):
  if(hidesn!=None and hidesn!=True):
   drawColorText(upc_img, 10, 2, barheight[1] + 2, upc_matches[0], barcolor[1]);
  drawColorText(upc_img, 10, 16, barheight[1] + 2, upc_matches[1], barcolor[1]);
  drawColorText(upc_img, 10, 62, barheight[1] + 2, upc_matches[2], barcolor[1]);
 drawColorLine(upc_img, 0, 10, 0, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 2, 10, 2, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 4, 10, 4, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 5, 10, 5, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 6, 10, 6, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 7, 10, 7, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 8, 10, 8, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 9, 10, 9, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 10, 10, 10, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 11, 10, 11, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 12, 10, 12, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 13, 10, 13, barheight[1], barcolor[0]);
 NumZero = 0; 
 LineStart = 14;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_barcolor_l = [0, 0, 0, 0, 0, 0, 0]; 
  left_barcolor_g = [1, 1, 1, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==0): 
   left_barcolor_l = [0, 0, 0, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_barcolor_l = [0, 0, 1, 1, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_barcolor_l = [0, 0, 1, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_barcolor_l = [0, 1, 1, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_barcolor_l = [0, 1, 0, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_barcolor_l = [0, 1, 1, 0, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_barcolor_l = [0, 1, 0, 1, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_barcolor_l = [0, 1, 1, 1, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_barcolor_l = [0, 1, 1, 0, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9):
   left_barcolor_l = [0, 0, 0, 1, 0, 1, 1];
   left_barcolor_g = [0, 0, 1, 0, 1, 1, 1];
  left_barcolor = left_barcolor_l;
  if(int(upc_matches[0])==1):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==2):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==3):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==4):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==5):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==6):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==7):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==8):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==9):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 56, 10, 56, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 57, 10, 57, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 58, 10, 58, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 59, 10, 59, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 60, 10, 60, barheight[1], barcolor[2]);
 NumZero = 0; 
 LineStart = 61;
 while (NumZero < len(RightDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  right_barcolor = [0, 0, 0, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==0): 
   right_barcolor = [1, 1, 1, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==1): 
   right_barcolor = [1, 1, 0, 0, 1, 1, 0];
  if(int(RightDigit[NumZero])==2): 
   right_barcolor = [1, 1, 0, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==3): 
   right_barcolor = [1, 0, 0, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==4): 
   right_barcolor = [1, 0, 1, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==5): 
   right_barcolor = [1, 0, 0, 1, 1, 1, 0];
  if(int(RightDigit[NumZero])==6): 
   right_barcolor = [1, 0, 1, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==7): 
   right_barcolor = [1, 0, 0, 0, 1, 0, 0];
  if(int(RightDigit[NumZero])==8): 
   right_barcolor = [1, 0, 0, 1, 0, 0, 0];
  if(int(RightDigit[NumZero])==9): 
   right_barcolor = [1, 1, 1, 0, 1, 0, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(right_barcolor)):
   if(right_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(right_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 103, 10, 103, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 104, 10, 104, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 105, 10, 105, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 106, 10, 106, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 107, 10, 107, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 108, 10, 108, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 109, 10, 109, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 110, 10, 110, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 111, 10, 111, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 112, 10, 112, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 113, 10, 113, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 114, 10, 114, barheight[0], barcolor[2]);
 if(supplement!=None and len(supplement)==2):
  upc_sup_img = draw_ean2_supplement(supplement,1,hideinfo,barheight,barcolor);
  upc_img.set_source_surface(upc_sup_img, 115, 0);
  upc_img.paint();
  del(upc_sup_img);
 if(supplement!=None and len(supplement)==5):
  upc_sup_img = draw_ean5_supplement(supplement,1,hideinfo,barheight,barcolor);
  upc_img.set_source_surface(upc_sup_img, 115, 0);
  upc_img.paint();
  del(upc_sup_img);
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (115 + addonsize) * int(resize), (barheight[1] + 8) * int(resize));
 new_upc_img = cairo.Context(new_upc_preimg);
 new_upc_img.set_source(upc_imgpat);
 new_upc_img.paint();
 del(upc_preimg);
 if(outfile is None or isinstance(outfile, bool)):
  return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_ean13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(upc,None,resize,hideinfo,barheight,barcolor);
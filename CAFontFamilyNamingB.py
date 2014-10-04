#FLM: CA Font Family Naming [B] V1.0
App = "CA Font Family Naming [B] V1.0"

""" 
		09/2010 Thomas Schostok - Cape Arcona Type Foundry
		www.cape-arcona.com

		De-Robofab-ed Version and additional coding by Karsten Luecke.

		USE AT YOUR OWN RISK!

		Description:
		This script changes the family and font names according to Karsten Lueckes 
		"Font Naming, Scheme [B], Page 7/8, Version 1.02"
		AS ONE DIFFERENCE: the script will style-link italic styles!
		
		See http://kltf.de/downloads/FontNaming-kltf.pdf for more information
		about the naming scheme. 				
		As stated in FontNaming-kltf.pdf, page 10, 'Naming Scheme [B] in Font Menus'
		this method will split up the family into single-font-families in the font menu
		in non-OT-savvy Windows applications.
		
		The script is straight forward to the conventions in the Font info panel in FontLab.
		Special names, weights, styles, etc. are not accepted.

		Whatever you like to do with the script - read the PDF first. :)				

 		Documentation:
		1. Preferences > Generating OpenType & TrueType
		   Select 'Use the OpenType names as menu names in Macintosh'
		   If you intend to generate CFF-OTF (T1) fonts, select also
		   'Use PostScript FontName als FullName on Windows'
		2. Open 'Font Info > Names and Copyright'
		3. In 'Family Name' enter family name of your font. For example: 'My Family'.
		   Do not enter a 'Family Name' that has the same name as the list in 'Weight'. 
		   For example 'My Ultra'. See notes for more information.
		4. Select 'Weight' (Regular, Light ExtraBold, whatever). 
		   Do not enter any other Weight that is not in the list!
		5. Uncheck 'Font is bold' even if your font is bold				
		6. If your font is italic (or oblique):
			Select 'Font is italic' (It's not necessary to select 'Font is bold')		   
		7. If your font is italic (or oblique): 
			'Metrics and Dimensions > Key Dimensions':
			- Set the 'Italic angle' to the corresponding italic angle of your font
			- Make sure that 'Slant angle' is always '0'
			- 'Copy Slant angle to Italic angle' is unchecked
				
		8. Run the script
		9. That's it
		10. Do not forget to generate 'Additional OpenType names' in FontLab after running the script
		
		Important notes:
		- Do not enter any other information in the "Names and Copyright". 
		  They will all be changed and overwritten automatically.
		- It's not necessary to select 'Font is bold'
		- The script tries to strip out any "Weight" entries that YOU entered in "Family Name"
		  to protect you from double entries (such "My Family Regular Regular") when you accidentally 
		  run the script more then one time. Problems may occur when you entered a "Family Name" 
		  that include a name from the "Weight" list. For example, a "Family Name" of: 
		  "My Ultra" will be renamed to "My Regular".
		  So please check your names first or don't use the script. :)
		
 		Requirements:
		- FontLab Studio 5

		NO WARRANTY.
		Always make copies of your .vfbs and run the script on the copies! Save .vfbs regularly.
		Script may damage .vfb files or crash FLS5. Script is provided as is. There is no warranty
		for performance or results obtained by using the script. The creator of the script will not
		be liable for any damages, claims or costs whatsoever or any direct, indirect, special,
		incidental or consequential damages, business interruption, nor for lost profits, savings or
		business information, arising out of any use of, or inability to use, the scripts.
"""

from FL import *
import math,os

def cleanName(name,removeAllSpaces=False):
	if removeAllSpaces:  return name.replace(" ","").strip()
	else:                return name.replace("  "," ").replace("  "," ").replace("  "," ").strip()
def regularizeName(name):
	if not name.strip(): return "Regular"
	else:                return name.strip()

def nameFont(fIdx):
		print "***********************************"

		italic  = "Italic"
		italicShort = "It"
		weights = [
			"UltraLight",
			"Thin",
			"ExtraLight",
			"Light",
			"Book",
			"Regular",
			"Normal",
			"Medium",
			"DemiBold",
			"SemiBold",
			"Bold",
			"ExtraBold",
			"Heavy",
			"Black",
			"Ultra",
			"UltraBlack",
			"Fat",
			"ExtraBlack",
			italic,
			italicShort,
		]
		
		f  = fl[fIdx]
		fn = cleanName(f.family_name)
		fw = cleanName(f.weight)
		fs = int(f.font_style)

		# safety web for not yet saved fonts:
		if f.file_name == None: filename = f.family_name.strip()
		else:                   filename = os.path.basename(f.file_name)

		# if any other style than italic or bold is set, skip font:
		if fs in [ 0,1,32,33,64 ]:
			print "PROCESSING: '%s' ..." % filename
		else:
			print "ERROR: You selected 'More Styles' than 'Font is italic' or 'Font is bold'.\nABORTED: Will not name font '%s'." % filename
			return

		# if any other weight than one of the standard ones, skip font:
		if fw not in weights:
			print "ERROR: You selected a non-FLS5-default weight.\nABORTED: Will not name font '%s'." % filename
			return
		if fw == "Normal":
			print "'Weight' changed from 'Normal' to 'Regular'."
			fw       = "Regular"
			f.weight = "Regular" # (cosmetics)

		# if family name includes italic/weight info, remove them:
		weightsTemp = [(len(w),w) for w in weights]
		weightsTemp.sort()
		weightsTemp.reverse()
		fnTemp     = "%s " % fn
		for weight in weightsTemp:
			fnTemp =           fnTemp.replace(" %s " % weight[1], " ")
		fnTemp     = cleanName(fnTemp)
		if fnTemp != fn:
			print "INFO: Removed styles from 'Family Name'."
		fn = fnTemp.strip()
		w = None; weight = None; weightsTemp = None; fnTemp = None; 

		# remove bold style info:
		if fs in [0,32]:
			if fw == "Regular":  fs = 64
			else:                fs =  0
		if fs in   [33]:         fs =  1
		f.font_style = int(fs)
		
		# keep italic style info:
		if fs == 1:
			italic      = " Italic"
			italicShort = " It"
		else:
			italic      = ""
			italicShort = ""

		# if Regular weight, remove string "Regular" except from PostScript name:
		fw_ps = fw.strip()
		if fw == "Regular":
			fw = ""
			if italic:
				fw_ps = ""
		# and in turn adjust short/long "Italic"/"It":
		if italic and not fw:
			italicShort = " Italic"

		# check of family name length check:
		lenstyle = max([len(w) for w in weights]) + 4 ; w = None
		lendiff  = 28-lenstyle-len(fn)
		if lendiff < 0:
			print "WARNING: Family Name '%s' is %s characters too long." % (fn,abs(lendiff))
		lenstyle = None; lendiff = None
		
		# check of italic settings:
		if fs in [1]:
			if not f.italic_angle:
				print "ERROR: 'Font is italic' checked, but 'Italic angle' is 0."
		if f.italic_angle:
			if fs in [0,64]:
				print "ERROR: 'Italic angle' is set, but 'Font is italic' is not checked."
		if f.slant_angle:
				print "WARNING: 'Slant angle' is %s but should be 0." % round(f.slant_angle,3)
	
		# Family Name = Family Name + Weight
		f.family_name = cleanName("%s %s" % (fn,fw))
		print "'Family Name':  [%s]" % f.family_name
	
		# Style Name = always "Regular" or "Italic"
		if fs == 1: f.style_name = "Italic"
		else:       f.style_name = "Regular"
		print "'Style Name':  [%s]" % f.style_name
	
		# PS Font Name = MyFamily-Style
		f.font_name = cleanName("%s-%s%s" % (fn,fw_ps,italicShort),removeAllSpaces=True)
		print "'PS Font Name':  [%s]" % f.font_name
		
		# Full = Family Name + Italic
		f.full_name = cleanName("%s%s" % (f.family_name,italicShort))
		print "'Full Name':  [%s]" % f.full_name
		
		# OT Family Name
		f.pref_family_name = cleanName(fn)
		print "'OT Family Name':  [%s]" % f.pref_family_name
	
		# OT Style Name
		f.pref_style_name = regularizeName(cleanName("%s%s" % (fw,italic)))
		print "'OT Style Name':  [%s]" % f.pref_style_name

		# Menu Name = empty
		f.menu_name = ""
		print "'Menu Name':  -empty-"
	
		# FOND Name = empty
		f.apple_name =""
		print "'FOND Name':  -empty-"
		
		# Mac Name = empty
		f.mac_compatible = ""
		print "'Mac Name':  -empty-"
		
		fl.UpdateFont(fIdx)

def renameFonts():
	
	if not len(fl):
		fl.Message("You need to open at least one font.",App)
		return

	yn = fl.Message("See script for documentation.\n\nChange font(s) now?",App,"Yes","No")
	if yn == 1:
	
		fl.output=""
		print "***********************************"
		print App
		for fIdx in range(len(fl)):
			named = nameFont(fIdx)
		print "***********************************"
		print "Done."
		print "Do not forget to generate 'Additional OpenType names' in FontLab!"

if __name__ == "__main__":
	renameFonts()
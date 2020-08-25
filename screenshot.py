from PIL import Image
import win32gui, win32ui, win32con,win32print

def ScreenshotByWin32API():
	hwnd = win32gui.GetDesktopWindow()
	hwndDC = win32gui.GetWindowDC(hwnd)  
	mfcDC=win32ui.CreateDCFromHandle(hwndDC)  
	saveDC=mfcDC.CreateCompatibleDC()  
	saveBitMap = win32ui.CreateBitmap()  
	w=win32print.GetDeviceCaps(hwndDC, win32con.DESKTOPHORZRES)
	h=win32print.GetDeviceCaps(hwndDC, win32con.DESKTOPVERTRES)
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  
	saveDC.SelectObject(saveBitMap)
	saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)
	#add cursor
	curFlags, curH, (curX, curY) = win32gui.GetCursorInfo()
	if curH!=0:
		saveDC.DrawIcon((curX, curY), curH)
	#see https://stackoverflow.com/questions/5999007/active-window-screenshot-with-python-pil-and-windows-api-how-to-deal-with-round
	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)
	im = Image.frombuffer('RGB',
	(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
	bmpstr, 'raw', 'BGRX', 0, 1)
	#release memory
	win32gui.DeleteObject(saveBitMap.GetHandle())
	saveDC.DeleteDC()
	mfcDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, hwndDC)
	return im
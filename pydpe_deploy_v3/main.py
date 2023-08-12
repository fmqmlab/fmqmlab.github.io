import asyncio
from js import document, console, Uint8Array, window, File
import io
from pyodide.ffi import create_proxy
import guido

async def on_click(event):

	#original code by Jeff Glass at https://jeff.glass/post/pyscript-image-upload/
	#refer to his website for more details (not the pyscript is constantly evolving so some elements from his code may have to be changed accordingly)
	#see the pyscript changelog if in doubt - https://docs.pyscript.net/latest/changelog.html

	#Display a processing messsage while all the data is being collected
	document.getElementById("graph-area").innerText = "Processing..."
	
	#read the image input <div> to retrieve the image
	#image_div = document.getElementById("user_image")
	file_list = document.getElementById("user_image").files
	first_item = file_list.item(0)

    #Get the data from the files arrayBuffer as an array of unsigned bytes
	array_buf = Uint8Array.new(await first_item.arrayBuffer())

	#BytesIO wants a bytes-like object, so convert to bytearray first
	bytes_list = bytearray(array_buf)
	my_bytes = io.BytesIO(bytes_list)

	dpe_mod_kwargs = {}

	image_file = my_bytes

	dpe_mod_kwargs['image_file'] = image_file

	kxmin = Element('kxmin').element.value
	kxmin = float(kxmin.strip())
	kxmax = Element('kxmax').element.value
	kxmax = float(kxmax.strip())	
	dpe_mod_kwargs['extent_x'] = [kxmin, kxmax]

	kymin = Element('kymin').element.value
	kymin = float(kymin.strip())
	kymax = Element('kymax').element.value
	kymax = float(kymax.strip())	
	dpe_mod_kwargs['extent_y'] = [kymin, kymax]

	theta_s = Element('theta_s').element.value
	theta_s = float(theta_s.strip())
	dpe_mod_kwargs['theta_s'] = theta_s

	phi_s = Element('phi_s').element.value
	phi_s = float(phi_s.strip())
	dpe_mod_kwargs['phi_s'] = phi_s

	rotation_s = Element('rotation_s').element.value
	rotation_s = float(rotation_s.strip())
	dpe_mod_kwargs['rotation_s'] = rotation_s

	hv = Element('hv').element.value
	hv = float(hv.strip())
	dpe_mod_kwargs['hv'] = hv

	wf = Element('wf').element.value
	wf = float(wf.strip())
	dpe_mod_kwargs['wf'] = wf

	FOV = Element('FOV').element.value
	FOV = float(FOV.strip())
	dpe_mod_kwargs['FOV'] = FOV

	guido.dpe_mod(**dpe_mod_kwargs)

upload_file = create_proxy(on_click)
document.getElementById("submit-button").addEventListener("click", upload_file)

import asyncio
from pydoll.browser import Chrome
from pydoll.browser.tab import Tab
from pydoll.browser.options import ChromiumOptions as Options
from bs4 import BeautifulSoup
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import os
import shutil

model = SentenceTransformer('all-MiniLM-L6-v2')


def handle_image(index:str):
    #  current directory
    current_dir = Path(os.path.join(os.getcwd(), "image_downloads"))
    # target directory
    target_dir = Path(os.path.join(os.getcwd(), "images"))

    for file in current_dir.iterdir():
        if file.is_file():
            new_name = f"{index}.jpg"
            new_path = target_dir / new_name  # new folder + new name
            # file.rename(new_path)
            shutil.move(str(file), str(new_path))
            print(f"Moved + renamed {file.name} → {new_path}")

async def main(query:str,index:str):
    
    try:
        
        options = Options()
        
        # options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        # Use existing profile
        # user_data_dir = r"C:\Users\admin\AppData\Local\Google\Chrome\User Data"
        # options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--profile-directory=Default")  # Use default profile
    
        # Optional: Prevent browser from closing automatically
        # options.add_experimental_option("detach", True)
        async with Chrome(options=options) as browser:   
            # id = await browser.get_browser_contexts()  
            tab = await browser.start()
            await tab.go_to("https://pixabay.com/")
            await asyncio.sleep(2)
            # select input element input[type="search"]
            search_box = await tab.query("input[type='search']")
            await search_box.type_text(query)
            await asyncio.sleep(2)
            await search_box.execute_script("""()=>{
                // Create a new KeyboardEvent for Enter
                var enterEvent = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                });

                // Dispatch the event on the currently focused element
                document.activeElement.dispatchEvent(enterEvent);
                            
                } """)
            await asyncio.sleep(3)
            
            await handle_pixabay_filter(tab)
            
            await asyncio.sleep(3)

            images = await tab.query('div[class^="results"] div[class^="verticalMasonry"] script[type="application/ld+json"]',find_all=True)
            suggestion_embedding = model.encode(query)
            selected_image = None
            best_score = -1
            
            for image in images:
                # print(image)
                image_data = await image.inner_html
                soup = BeautifulSoup(image_data,features="html.parser")
                image_str_obj = soup.find('script').text
                image_object = json.loads(image_str_obj)
                image_embedding = model.encode(image_object["name"])
                similarity = util.cos_sim(suggestion_embedding, image_embedding).item()
                print(f"Suggestion: '{"mountain peak silhouette"}' | Image: {image_object['contentUrl']} | Score: {similarity:.3f}")
                if similarity > best_score:
                    best_score = similarity
                    selected_image = image_object
                
            print("\n=== BEST MATCH ===")
            print(f"selected Image a tag href {selected_image['acquireLicensePage']}")
            print(f"Selected Image: {selected_image['contentUrl']} with score {best_score:.3f}")
            
            await asyncio.sleep(3)
            
            await (await tab.query(f'a[href="{selected_image['acquireLicensePage']}"]')).click()
            
            await asyncio.sleep(3)
            
            await (await tab.query('button[class^="fullWidthTrigger"]')).click()
            
            # div[class="container--YKYLB container--gwuMt fullWidthContainer--a8QAe"] > div > div > div > div > label:last-child
            # div[class^="container--YK"] > div > div > div > div > label:last-child
            await (await tab.query('div[class^="container--YK"] > div > div > div > div > label:last-child')).click()
            # .buttons--cqw3Y > a:first-of-type
            # await asyncio.sleep(20)
            current_dir = os.path.join(os.getcwd(),'image_downloads')
            
            try:
                async with tab.expect_download(keep_file_at=current_dir,timeout=15) as dl:
                    await (await tab.query('.buttons--cqw3Y > a:first-of-type')).click()
                    data = await dl.read_bytes()
                    print('Saved at:', dl.file_path)
                
            except Exception as e:
                print(e)
            handle_image(index=index)
            # await asyncio.sleep(2000)
    except Exception as e:
        #  handle browser level error
        print(e)
    


async def handle_pixabay_filter(tab:Tab):
    try:
        # photo => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button')).click()
        await asyncio.sleep(2)
            # dropdown photo click => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)')).click()
        await asyncio.sleep(2)           
        # horizontal => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button')).click()
        await asyncio.sleep(2)         
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)')).click()
        await asyncio.sleep(2)         
        # authencity => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button')).click()
        await asyncio.sleep(2)           
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await(await tab.query('div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)')).click()
        await asyncio.sleep(2)
    except Exception as e:
        print(e)



# async def download_image():
#     # https://cdn.pixabay.com/photo/2020/10/23/09/02/mountain-5678172_1280.jpg 
#     pass


if __name__ == "__main__":
    with open("output.json", "r", encoding="utf-8") as f:
        transcription = json.load(f)
    segments = transcription['segments']
    
    for segement in segments:
        asyncio.run(main(query=segement['image_suggestion'][0],index=str(segement['id'])))
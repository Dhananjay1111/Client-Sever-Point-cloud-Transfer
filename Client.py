import pickle
import asyncio
import websockets
import pandas as pd


async def PCT_pointcloud_loader():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        pointcloud_array = []
        with open(r'X:\Internship\Point Cloud technology\PCT\Strausberg\Strausberg\GUI_trial set\New folder\399000_5829000.csv',newline='') as pointcloud_csv_file:
            import csv
            try:
                reader = csv.reader(pointcloud_csv_file)
                for row in reader:
                    pointcloud_array.append((row))
            except IOError:
                print("Could not read file:", pointcloud_csv_file)
        pointcloud_serialized = pickle.dumps(pointcloud_array)
        await websocket.send(pointcloud_serialized)
        print(f'Point cloud data Sent to server')

        ######################
        #Data sent to server
        ######################

        processed_pointcloud_serialized= await websocket.recv()
        processed_pointcloud_array = pickle.loads(processed_pointcloud_serialized)
        processed_pointcloud_array_dataframe = pd.DataFrame(processed_pointcloud_array)
        try:
            processed_pointcloud_array_dataframe.to_csv("Predicted_pointcloud.csv", index=False)
            print(f"< Whole process is done")
        except:
            print("Something went wrong, couldn't write the file")

asyncio.get_event_loop().run_until_complete(PCT_pointcloud_loader())
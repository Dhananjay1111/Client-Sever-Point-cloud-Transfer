import asyncio
import websockets
import pickle
import pandas as pd


async def PCT_pointcloud_processor(websocket, path):
    pointcloud_serialized = await websocket.recv()
    pointcloud_array = pickle.loads(pointcloud_serialized)
    print(f'Data received at server')
    #####
    point_cloud_to_be_processed_array_dataframe = pd.DataFrame(pointcloud_array)
    try:
        point_cloud_to_be_processed_array_dataframe.to_csv("To_be_Predicted_pointcloud.csv", index=False)
        print(f"< point cloud to be predicted is saved at pcnn directory")
    except:
        print("Something went wrong, couldn't write the file")

    ###############
    # add some kind of processing here
    ###############

    pointcloud_array = []
    with open("To_be_Predicted_pointcloud.csv", newline='') as pointcloud_csv_file:
        import csv
        try:
            reader = csv.reader(pointcloud_csv_file)
            for row in reader:
                pointcloud_array.append((row))
        except IOError:
            print("Could not read file:", pointcloud_csv_file)
    ###############
    processed_pointcloud = pickle.dumps(pointcloud_array)
    await websocket.send(processed_pointcloud)
    print(f"> processed point cloud sent back to client")


start_server = websockets.serve(PCT_pointcloud_processor, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

import matplotlib.pyplot as plt
import imageio
import os


def generate_scenario_gif(data, start_frame, end_frame, scenario_name, output_file):

    frames = []

    window_data = data[
        (data["Frame_ID"] >= start_frame) &
        (data["Frame_ID"] <= end_frame)
    ]

    unique_frames = sorted(window_data["Frame_ID"].unique())

    # choose ego vehicle (first vehicle in window)
    ego_vehicle = window_data["Vehicle_ID"].iloc[0]

    # detect lane change vehicle
    lane_changes = window_data.groupby("Vehicle_ID")["Lane_ID"].nunique()
    changing_vehicle = None

    for vid, count in lane_changes.items():
        if count > 1:
            changing_vehicle = vid
            break

    y_min = window_data["Local_Y"].min() - 10
    y_max = window_data["Local_Y"].max() + 10

    lanes = sorted(window_data["Lane_ID"].unique())

    for frame in unique_frames:

        frame_data = window_data[window_data["Frame_ID"] == frame]

        plt.figure(figsize=(5,8))

        # draw lane lines
        for lane in lanes:
            plt.axvline(x=lane, linestyle="--", color="gray")

        for _, row in frame_data.iterrows():

            vehicle_id = row["Vehicle_ID"]
            lane = row["Lane_ID"]
            y = row["Local_Y"]

            # choose vehicle color
            if vehicle_id == ego_vehicle:
                color = "red"
                size = 80

            elif vehicle_id == changing_vehicle:
                color = "orange"
                size = 80

            else:
                color = "blue"
                size = 40

            plt.scatter(lane, y, color=color, s=size)

            plt.text(
                lane,
                y,
                str(int(vehicle_id)),
                fontsize=8,
                ha="center",
                color="black"
            )

        # draw trajectory lines
        for vid, group in window_data.groupby("Vehicle_ID"):

            if vid == ego_vehicle:
                color = "red"

            elif vid == changing_vehicle:
                color = "orange"

            else:
                color = "lightblue"

            plt.plot(
                group["Lane_ID"],
                group["Local_Y"],
                color=color,
                alpha=0.4
            )

        plt.title(f"{scenario_name} | Frame {frame}")

        plt.xlabel("Lane")
        plt.ylabel("Road Position")

        plt.xlim(min(lanes)-1, max(lanes)+1)
        plt.ylim(y_min, y_max)

        filename = f"_temp_frame_{frame}.png"

        plt.savefig(filename)
        plt.close()

        frames.append(imageio.imread(filename))

    imageio.mimsave(output_file, frames, duration=0.2)

    # cleanup temporary files
    for frame in unique_frames:
        temp = f"_temp_frame_{frame}.png"
        if os.path.exists(temp):
            os.remove(temp)
"""
3 scenarios we are implementing:
    1. Car following
    2. Lane change
    3. Cut-in
"""


def detect_lane_change(window):
    """
    Lane change if:
    - Lane_ID changes
    - noticeable lateral movement
    """
    lanes = window["Lane_ID"]

    if lanes.nunique() > 1:
        return True

    return False


def detect_car_following(window):
    """
    Detect car following using vehicles present in the same frame
    """

    ego_lane = window.iloc[0]["Lane_ID"]
    ego_y = window.iloc[0]["Local_Y"]
    ego_v = window.iloc[0]["v_Vel"]

    same_lane = window[window["Lane_ID"] == ego_lane]

    for i in range(len(same_lane)):

        other_y = same_lane.iloc[i]["Local_Y"]
        other_v = same_lane.iloc[i]["v_Vel"]

        dist = abs(other_y - ego_y)
        vel_diff = abs(other_v - ego_v)

        if 0 < dist < 30 and vel_diff < 5:
            return True

    return False


def detect_cutin(window):
    """
    Detect another vehicle entering ego lane
    """

    ego_lane = window.iloc[0]["Lane_ID"]
    ego_y = window.iloc[0]["Local_Y"]

    vehicles = window["Vehicle_ID"].unique()

    for vehicle in vehicles:

        vehicle_data = window[window["Vehicle_ID"] == vehicle]

        if len(vehicle_data) < 2:
            continue

        start_lane = vehicle_data.iloc[0]["Lane_ID"]
        end_lane = vehicle_data.iloc[-1]["Lane_ID"]

        if start_lane != ego_lane and end_lane == ego_lane:

            other_y = vehicle_data.iloc[-1]["Local_Y"]

            if other_y > ego_y and abs(other_y - ego_y) < 30:
                return True

    return False


def classify_window(window):

    lane_changes = window.groupby("Vehicle_ID")["Lane_ID"].nunique()

    if (lane_changes > 1).any():

        if window["Vehicle_ID"].nunique() > 20:
            return "Cut-In"

        return "Lane Change"

    if window["Vehicle_ID"].nunique() > 1:
        return "Car Following"

    return "Other"
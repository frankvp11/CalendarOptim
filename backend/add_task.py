

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from icalendar import Calendar
import datetime
import pytz
from model.user import User 
from model.event import Event
from model.stat import Stat
from dateutil.parser import parse

class GapFinder():
    def __init__(self, events) -> None:
        self.gaps_by_date = {}
        self.events = events

    def get_gaps(self, now, num_days=7):


        today = now.date()
        events_by_date = {}
        for start, end in self.events:
            if start.date() not in events_by_date:
                events_by_date[start.date()] = []
            events_by_date[start.date()].append((start.time(), end.time()))

        for i in range(num_days):
            current_date = today + datetime.timedelta(days=i)
            
            if current_date == today:
                gaps = [(max(datetime.time(5, 0), now.time()), datetime.time(22, 0))]
            else:
                gaps = [(datetime.time(5, 0), datetime.time(22, 0))]
            
            day_events = events_by_date.get(current_date, [])
            
            for event_start, event_end in sorted(day_events):
                new_gaps = []
                
                for gap_start, gap_end in gaps:
                    if event_end <= gap_start:
                        new_gaps.append((gap_start, gap_end))
                    elif event_start >= gap_end:
                        new_gaps.append((gap_start, gap_end))
                    elif event_start <= gap_start and event_end > gap_start:
                        new_gaps.append((event_end, gap_end))
                    elif event_start < gap_end and event_end >= gap_end:
                        new_gaps.append((gap_start, event_start))
                    elif event_start > gap_start and event_end < gap_end:
                        new_gaps.append((gap_start, event_start))
                        new_gaps.append((event_end, gap_end))

                gaps = new_gaps

            gap_dict = {}
            for start, end in gaps:
                gap_length = (datetime.datetime.combine(current_date, end) - datetime.datetime.combine(current_date, start)).total_seconds() / 3600  # hours
                gap_dict[gap_length] = (start, end)
            self.gaps_by_date[current_date] = gap_dict

        return self.gaps_by_date


class Scheduler():
    def __init__(self, events, tasks) -> None:
        self.events = events
        self.gapfinder = GapFinder(events=self.events)
        self.gaps = self.gapfinder.get_gaps(now=datetime.datetime.now(pytz.timezone('America/Toronto')))
        
        self.tasks = sorted(tasks, key=lambda x : x[1])

    def knapsack(self, bucket_volume):
        scale_factor = 100
        bucket_volume_scaled =  round(bucket_volume* scale_factor)
        task_volumes_scaled = [(task[0], int(task[1].total_seconds() * scale_factor / 3600)) for task in self.tasks]

        n = len(task_volumes_scaled)
        dp = [[0 for _ in range(bucket_volume_scaled + 1)] for _ in range(n + 1)]

        for i in range(n + 1):
            for w in range(bucket_volume_scaled + 1):
                if i == 0 or w == 0:
                    dp[i][w] = 0    
                elif task_volumes_scaled[i-1][1] <= w:
                    dp[i][w] = max(dp[i-1][w], task_volumes_scaled[i-1][1] + dp[i-1][w-task_volumes_scaled[i-1][1]])
                else:
                    dp[i][w] = dp[i-1][w]

        w = bucket_volume_scaled
        chosen_tasks = []

        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                chosen_tasks.append(task_volumes_scaled[i-1][0])
                w -= task_volumes_scaled[i-1][1]

        # Return the used volume as a timedelta
        used_volume_timedelta = datetime.timedelta(hours=dp[n][bucket_volume_scaled] / scale_factor)
        return used_volume_timedelta, chosen_tasks

    

    def filter_packages(self, bucket_volume):
        bucket_volume = datetime.timedelta(hours=bucket_volume)
        return [task for task in self.tasks if task[1] <= bucket_volume]



    def solve(self):
        temp_information = []

        for day in self.gaps:
            gaps = self.gaps[day].keys()
            for gap in gaps:
                if not self.tasks:
                    break
                applicable_tasks = self.filter_packages(gap)
                used_volume, tasks_used = self.knapsack(gap)
                wasted_volume = gap - (used_volume.total_seconds() / 3600)

                # Initial start time for this gap
                current_start_time = datetime.datetime.combine(day, self.gaps[day][gap][0])

                if (wasted_volume == 0 or day == datetime.datetime.now().date()) and self.tasks and tasks_used:
                    for task_name in tasks_used:
                        task_duration = next((duration for name, duration in self.tasks if name == task_name), None)
                        if task_duration:
                            # End time based on the task's duration

                            current_end_time =  current_start_time + task_duration
                            # print(datetime.datetime.combine(day, current_start_time))
                            yield ([task_name], (current_start_time, current_end_time), day)
                            # Adjusting for the next task
                            current_start_time = current_end_time

                    # Remove used tasks from the list
                    self.tasks = [task for task in self.tasks if task[0] not in tasks_used]

                elif self.tasks:
                    temp_information.append((wasted_volume, tasks_used, day, self.gaps[day][gap]))

            if not self.tasks:
                break

            if temp_information:
                temp_information = sorted(temp_information, key=lambda x: x[0])
                temp_information = [temp for temp in temp_information if temp[1]]

                while self.tasks and temp_information:
                    top = temp_information[0]
                    current_start_time = datetime.datetime.combine(day, top[-1][0])  # Reset the start time for each gap in temp_information
                    for task in top[1]:
                        if any(t == task for t, _ in self.tasks) and task:
                            task_duration = next((duration for name, duration in self.tasks if name == task), None)
                            if task_duration:
                                # End time based on the task's duration
                                current_end_time =  current_start_time + task_duration
                                yield ([task], (current_start_time, current_end_time), top[-2])
                                # Adjusting for the next task
                                current_start_time = current_end_time

                            # Remove used tasks from the list
                            task_to_remove = next((t for t in self.tasks if t[0] == task), None)
                            if task_to_remove:
                                self.tasks.remove(task_to_remove)

                    temp_information.remove(top)

                                
                    # Print remaining tasks that couldn't be scheduled
        if self.tasks:
                    print(f"Remaining tasks that couldn't be scheduled: {self.tasks}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import firebase_admin
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "accountkey.json"





def get_or_create_user_event(username, start, end, summary, existing_events, regular_event=True):
    user = User.collection.get(username)
    event_identifier = f"{start}-{end}-{summary}"

    # Check if the event exists in the user's events
    if event_identifier not in existing_events:
        event = Event(start=start, end=end, summary=summary, regular_event=regular_event)
        user.events.append(event)

        # Assuming you want to add a stat every time an event is added
        stats = Stat(data_point=1)
        user.stats.append(stats)
        
        # Add the new event's identifier to the set
        existing_events.add(event_identifier)

    return user, existing_events


# from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SA, SU

# weekdays = {
#     "MO": MO,
#     "TU": TU,
#     "WE": WE,
#     "TH": TH,
#     "FR": FR,
#     "SA": SA,
#     "SU": SU
# }


# @app.get("/getEvents")


async def get_events(url: str, duration: str = "monthly"):

    start = datetime.datetime.now()
    try:
        response = requests.get(url)
        cal = Calendar.from_ical(response.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch and parse the calendar")
    print(( datetime.datetime.now()-start).total_seconds())
    now = datetime.datetime.now(pytz.timezone('America/Toronto')) - datetime.timedelta(days=30)
    start = datetime.datetime.now()
    end_date = now + datetime.timedelta(days=60)
    event_times = []
    for event in cal.walk('vevent'):
        dtstart = event.get('dtstart').dt
        dtend = event.get('dtend').dt
        rrule = event.get('rrule')
        summary = event.get("SUMMARY")
        if rrule:
            freq = rrule.get('FREQ')[0]
            until = rrule.get('UNTIL')[0]
            byday = rrule.get('BYDAY')
            if freq == "WEEKLY":
                current_start = dtstart
                while current_start <= min(until, end_date):
                    if now <= current_start:
                        weekday = current_start.strftime('%A')[:2].upper()
                        if weekday in byday:
                            event_times.append((current_start, current_start + (dtend-dtstart), summary))
                    current_start += datetime.timedelta(days=1)
        else:
            if now <= dtstart <= end_date:
                event_times.append((dtstart, dtend, summary))
    print((datetime.datetime.now()-start).total_seconds())
    event_times = list(set(event_times))
    event_times.sort(key=lambda x: x[0])
    event_times = [(event1.astimezone(pytz.timezone('America/Toronto')), event2.astimezone(pytz.timezone('America/Toronto')), str(summary)) for (event1, event2, summary) in event_times]
    

    start = datetime.datetime.now()
    user = User.collection.get("Frank")
    
    # If user doesn't exist, create one with empty events and stats lists
    if not user:
        user = User(id="Frank", events=[], stats=[])

    # Load all current events into a set for fast lookup
    existing_events = set(f"{ev.start}-{ev.end}-{ev.summary}" for ev in user.events)


    for start_time, end_time, summary in event_times:
        # Store to database
        get_or_create_user_event("Frank", start_time, end_time, summary, existing_events, True)
    print((datetime.datetime.now()-start).total_seconds())
    return {"event_times": event_times}





# @app.get("/checkDatabase")
async def check_database(username:str="Frank"):
    
    today = datetime.datetime.now(pytz.timezone('America/Toronto')).date() - datetime.timedelta(days=35)
    end_date = today + datetime.timedelta(days=70)

    # Fetch user events based on the document ID (username)
    user = User.collection.get(username)
    if not user or not user.events:
        return {"events3": []}

    # Filter events based on the date range
    events_in_range = [e for e in user.events if e.start.date() >= today and e.start.date() < end_date]

    # Format the events
    formatted_events = []
    for e in events_in_range:
        start_dt = e.start.astimezone(  pytz.timezone('America/Toronto'))
        end_dt = e.end.astimezone(  pytz.timezone('America/Toronto'))

        formatted_events.append({
            "title": str(e.summary),
            "start": str(start_dt.strftime('%Y-%m-%d %H:%M:%S')),
            "end": str(end_dt.strftime('%Y-%m-%d %H:%M:%S')),
        })
        # print(e.summary)

    return {"events3": formatted_events}





# @app.post("/determineBestTime")
def determine_best_time(tasks: list[dict],extra_tasks=[],  username="Frank"):
    tasks = [(task["name"], datetime.timedelta(hours=task['duration'])) for task in tasks]
    today = datetime.datetime.now(pytz.timezone('America/Toronto'))

    start_time = today.replace(hour=5, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=22, minute=0, second=0, microsecond=0)

    # Fetch user and its events
    user = User.collection.get(username)  # You might want to change this hardcoded username
    events_today = [e for e in user.events if e.start >= start_time and e.start < (today + datetime.timedelta(days=7))]

    events = [(e.start.astimezone(pytz.timezone("America/Toronto")), e.end.astimezone(pytz.timezone("America/Toronto"))) for e in events_today]
    for task in extra_tasks:
        events.append((parse(task.get("start")).astimezone(pytz.timezone("America/Toronto")), parse(task.get("end")).astimezone(pytz.timezone("America/Toronto"))))

    day_start = datetime.datetime.now().replace(hour=5, minute=0).replace(tzinfo=pytz.timezone('America/Toronto'))
    day_end = datetime.datetime.now().replace(hour=22, minute=0).replace(tzinfo=pytz.timezone('America/Toronto'))
    scheduler = Scheduler(events, tasks)
    total = []
    for answer in scheduler.solve():
        task_names = answer[0]
        start, end = answer[1]
        date = answer[2]
        if len(task_names) > 1:
            for task_ in task_names:
                temp_start, temp_end = datetime.datetime.combine(date, start), datetime.datetime.combine(date, start) +next((t for t in tasks if t[0] == task_names[0]), None)[1]
                start = temp_end.time()
                total.append((task_, temp_start, temp_end))
        else:
            start, new_end = (start, start + next((t for t in tasks if t[0] == task_names[0]), None)[1])
            total.append((task_names[0], start, new_end))
    # for ans in total:
    #     print(ans)

    return [{"best_time": {"start": start, "end": end, "summary":task }} for (task, start, end) in total]




def getStats(username: str="Frank"):
    
    user = User.collection.get(username)
    if not user:
        return {"error": "User not found"}

    past_regular_events_count = sum(1 for ev in user.events if ev.end.replace(tzinfo=None) < datetime.datetime.now() and ev.start.replace(tzinfo=None) > datetime.datetime.now()-datetime.timedelta(days=30) and ev.regular_event)
    past_non_regular_events_count = sum(stat.data_point for stat in user.stats)

    return {
        "past_regular_events": past_regular_events_count,
        "past_non_regular_events": past_non_regular_events_count
    }

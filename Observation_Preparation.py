from astroplan import download_IERS_A
from astroplan import moon_illumination
from astropy.coordinates import get_sun, get_moon, get_body
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.coordinates import EarthLocation
import pytz
from astroplan import Observer, FixedTarget
from astropy.utils.iers import conf
from astroplan.plots import plot_finder_image
from astroquery.skyview import SkyView
from astroplan import (AltitudeConstraint, AirmassConstraint,
                       AtNightConstraint, MoonSeparationConstraint)
from astroplan import is_observable, is_always_observable, months_observable
from astropy.table import Table

conf.auto_max_age = None
download_IERS_A()


def observatory_setup():
    latitude = 18.51773 * u.deg
    longitude = 73.81488 * u.deg
    elevation = 560 * u.m
    location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    # You can optionally specify a time zone as well.
    # A list of timezones can be found at https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    aryabhatta = Observer(location=location, timezone='Asia/Kolkata',
                          name="Aryabhatta", description="MIT Observatory")
    return aryabhatta


now = Time.now()


def observer_info(observer=observatory_setup()):
    observer_info = pd.DataFrame(columns=["Name", "Date and Time"])
    sunset_ioMIT = observer.sun_set_time(now, which="nearest")
    eve_twil_ioMIT = observer.twilight_evening_astronomical(
        now, which="nearest")
    midnight_ioMIT = observer.midnight(now, which="nearest")
    morn_twil_ioMIT = observer.twilight_morning_astronomical(
        now, which="nearest")
    sunrise_ioMIT = observer.sun_rise_time(now, which="next")

    # Adding rows to the Output info file database
    observer_info.loc[0] = ["Nearest Sunset Time", sunset_ioMIT.iso]
    observer_info.loc[1] = [
        "Nearest Evening Twilight Time", eve_twil_ioMIT.iso]
    observer_info.loc[2] = ["Nearest Midnight Time", midnight_ioMIT.iso]
    observer_info.loc[3] = [
        "Nearest Morning Twilight Time", morn_twil_ioMIT.iso]
    observer_info.loc[4] = ["Next Sunrise Time", sunrise_ioMIT.iso]

    observer_info.to_csv("Observer_Information.csv")


def Messier_Objects():
    target_names = ['vega', 'polaris', 'm1', 'm42', 'm55']
    targets = [FixedTarget.from_name(target) for target in target_names]
    names = []
    ra = []
    dec = []
    airmass = []

    for i in range(len(targets)):
        names.append(targets[i].name)
        ra.append(targets[i].ra)
        dec.append(targets[i].dec)
        airmass.append(observatory_setup().altaz(
            observatory_setup().midnight(now, which="nearest"), targets[i]))

    pd.DataFrame({'name': names, 'ra': ra, 'dec': dec,
                 'airmass': airmass}).to_csv('Messier_Objects.csv')


def Solar_Objects():
    midnight_ioMIT = observatory_setup().midnight(now, which="nearest")
    target_names = ['jupiter', 'mars', 'venus', 'saturn', 'neptune', 'moon']
    targets = [get_body(target, midnight_ioMIT) for target in target_names]
    ra = []
    dec = []
    for i in range(len(targets)):
        ra.append(targets[i].ra)
        dec.append(targets[i].dec)
    pd.DataFrame({'name': target_names, 'ra': ra, 'dec': dec}
                 ).to_csv('Solar_Objects.csv')


def finder(target_names):
    targets = [FixedTarget.from_name(target) for target in target_names]
    for i in targets:
        plot_finder_image(i, fov_radius=20 * u.arcmin)


def Observable(observer=observatory_setup()):
    target_names = ['vega', 'polaris', 'm1', 'm42', 'm55']
    targets = [FixedTarget.from_name(target) for target in target_names]
    t_start = observer.twilight_evening_astronomical(
        now, which="nearest")
    t_end = observer.twilight_morning_astronomical(
        now, which="nearest")
    constraints = [AltitudeConstraint(15*u.deg, 84*u.deg),
                   AirmassConstraint(3), AtNightConstraint.twilight_civil(), MoonSeparationConstraint(min=10 * u.deg)]
    t_range = Time([t_start - 0.5 * u.hour, t_end + 0.5 * u.hour])
    ever_observable = is_observable(
        constraints, observatory_setup(), targets, time_range=t_range)
    # print(ever_observable)
    always_observable = is_always_observable(
        constraints, observatory_setup(), targets, time_range=t_range)
    # print(always_observable)
    observability_table = Table()
    observability_table['targets'] = [target.name for target in targets]
    observability_table['ever_observable'] = ever_observable
    observability_table['always_observable'] = always_observable
    # print(observability_table)
    observability_table.write(
        "Observability_Table.csv", format="csv", overwrite=True)


observer_info()
Messier_Objects()
Solar_Objects()
finder(target_names=['vega', 'polaris', 'm1', 'm42', 'm55'])
Observable()


print("OK!")

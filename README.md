# Pipeline

## Observation Run
This script sets up an observatory location using the latitude, longitude, and elevation, as well as a timezone. It then uses the Observer class from astroplan to find the nearest sunset, evening astronomical twilight, midnight, morning astronomical twilight, and next sunrise times, and writes these times to a CSV file named "Observer_Information.csv".
It also defines two functions, Messier_Objects and Solar_Objects, that use the FixedTarget.from_name and get_body functions from astroplan and astropy respectively to get the coordinates, airmass, and other information for different solar and Messier objects and writes this information to CSV files named "Messier_Objects.csv" and "Solar_Objects.csv" respectively.
It also uses astroquery's skyview for a Finder chart of the object and astroplan's constraint for observability of objects.

# Pipeline

## Observation Run
This script sets up an observatory location using the latitude, longitude, and elevation, as well as a timezone. It then uses the Observer class from astroplan to find the nearest sunset, evening astronomical twilight, midnight, morning astronomical twilight, and next sunrise times, and writes these times to a CSV file named "Observer_Information.csv".
It also defines two functions, Messier_Objects and Solar_Objects, that use the FixedTarget.from_name and get_body functions from astroplan and astropy respectively to get the coordinates, airmass, and other information for different solar and Messier objects and writes this information to CSV files named "Messier_Objects.csv" and "Solar_Objects.csv" respectively.
It also uses astroquery's skyview for a Finder chart of the object and astroplan's constraint for observability of objects.

## Image Reduction
This script sets up a directory structure with folders for bias frames, flat frames, and science frames. It then defines several functions to perform various steps of image processing on the science frames.
The function masterBiasFrame takes a folder containing bias frames as input, reads in all the bias frames, and computes the median of these frames to create a master bias frame.
The function masterFlatFrame takes a folder containing flat frames as input, reads in all the flat frames, subtracts the master bias frame, normalizes the resulting frames, and computes the mean of these frames to create a master flat frame.
The function processingData takes a list of science frames as input, reads in each science frame, subtracts the master bias frame and divides by the master flat frame to perform bias and flat correction, and then saves these corrected frames in a new folder called "processing".
The function cosmicCorrection takes a list of science frames as input, applies cosmic ray correction on the frames using astroscrappy library and saves the cleaned frames in the processing folder
The script also calls astroquery's skyview for a Finder chart of the object and astroplan's constraint for observability of objects.
It also uses pyregion library to create a ds9 region file of the objects.
It also uses shutil library to copy the files in processing folder to another location.

## Photometry
This script is used to match a catalog of sources with a specific image. The script takes an image file path as an input and uses astropy library to read the image and its header, then it uses the WCS (World Coordinate System) module to extract the coordinates of the center of the image. The script also defines several functions to perform various steps of image processing on the science frames.
The get_table_from_ldac function takes a filename and a frame number as input and returns the table data from the specified frame of the file.
The open_fits function opens the image specified by the input file path, reads the data and header of the image and computes some image statistics for scaling the image plot.
The create_wcs function takes the data and header of the image as input, stores the image WCS into an object, gets the RA and Dec of the center of the image and sets the box size to search for catalog stars.
The catalog_quering function takes the center coordinates of the image, box size, and a max magnitude of sources to be cross-matched against as inputs, queries Vizier for the sources in the specified region and returns the queried catalog.
The wld_coord_2_img_coord function takes the WCS object and queried catalog as inputs, converts the world coordinates of the catalog sources to image coordinates, filters the sources which are close to the edges of the image and returns the final catalog of sources matched with the image.
The script uses the Vizier module of astroquery library for querying the catalog and pandas library for data manipulation.

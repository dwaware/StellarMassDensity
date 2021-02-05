display_height = 1000
# in pixels

display_width = 1200
# in pixels

map_size = 1000
# in pixels

map_scale = 100
# in ly / pixel

galaxy_size = map_size*map_scale
# display_size * map_scale

core_radius = 10000
# core radius in light years -- actual core is 1/10th the size (1000 ly) the rest is a transitional ramp

galaxy_height = 1000
# core height in light years

xoff = int(map_size/2)
# half the display size in pixels

yoff = int(map_size/2)
# half the display size in pixels

mmxoff = 1010

mmyoff = 10

# colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
background = white
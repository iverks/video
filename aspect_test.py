from manim import *

fake_compression = 4
config["pixel_width"] = 1080 // fake_compression
config["pixel_height"] = 1920 // fake_compression


class Intro(Scene):
    def construct(self):
        electron_gun_top = Cylinder(direction=UP)
        electron_gun_bottom = Cone(direction=DOWN)
        electron_gun_top.shift(UP * 2)
        electron_gun = VMobject()
        electron_gun.add(electron_gun_bottom)
        electron_gun.add(electron_gun_top)

        self.play(Create(electron_gun))

        self.wait(1)

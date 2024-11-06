import manim
from manim import *

C_ELECTRON = GREEN
C_E_GUN = GOLD
C_E_GUN_2 = GOLD_B
C_LENS = BLUE_C
C_LENS_2 = BLUE_B
C_SAMPLE = GRAY_BROWN
SMALL_FONT_SIZE = 24

egun_2d_kwargs = {
    "stroke_color": C_E_GUN_2,
    "fill_color": C_E_GUN,
    "fill_opacity": 0.4,
}

lens_2d_kwargs = {
    "stroke_color": C_LENS_2,
    "fill_color": C_LENS,
    "fill_opacity": 0.4,
}

sample_2d_kwargs = {
    "stroke_color": C_SAMPLE,
    "fill_color": C_SAMPLE,
    "fill_opacity": 0.4,
}


electron_gun_top = Rectangle(height=2, width=2, **egun_2d_kwargs)
electron_gun_top.shift(UP * 4)
electron_gun_bottom = Polygon(UP * 3 + LEFT, UP * 3 + RIGHT, UP * 2, **egun_2d_kwargs)

lens_l = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
lens_l.shift(LEFT * 1.5)
lens_r = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
lens_r.shift(RIGHT * 1.5)
lens = VGroup(lens_l, lens_r)

sample_holder = Rectangle(width=2, height=0.5, **sample_2d_kwargs)
sample_holder.shift(DOWN * 2.75)

electron_gun_rect = RoundedRectangle(
    height=3,
    width=4,
    corner_radius=0.5,
    stroke_color=C_E_GUN,
)
electron_gun_rect.shift(UP * 3)
electron_gun_label = Text(
    "Electron gun", font_size=SMALL_FONT_SIZE, color=C_E_GUN
).next_to(electron_gun_rect)

lens_sys_rect = RoundedRectangle(
    height=2.0,
    width=4,
    corner_radius=0.5,
    stroke_color=C_LENS,
)
lens_sys_label = Text("Lens system", font_size=SMALL_FONT_SIZE, color=C_LENS).next_to(
    lens_sys_rect
)

sample_rect = RoundedRectangle(
    height=2.5,
    width=4,
    corner_radius=0.5,
    stroke_color=C_SAMPLE,
)
sample_rect.shift(DOWN * 2.75)
sample_label = Text("Sample", font_size=SMALL_FONT_SIZE, color=C_SAMPLE).next_to(
    sample_rect
)

lens_lens = ArcPolygon(
    LEFT * 1.4,
    RIGHT * 1.4,
    radius=4,
    fill_opacity=0.3,
    fill_color=C_LENS,
    stroke_opacity=0.0,
    arc_config={"stroke_width": 1, "stroke_color": C_LENS},
)


class Overview(MovingCameraScene):
    def construct(self):
        self.add(electron_gun_top, electron_gun_bottom, lens, sample_holder)
        self.wait(1)

        # * The electron microscope consists of three main parts
        # The electron gun, the lens system and the sample and sample holder
        self.play(
            FadeIn(
                electron_gun_rect,
                electron_gun_label,
                lens_sys_rect,
                lens_sys_label,
                sample_rect,
                sample_label,
            )
        )

        self.wait(2)

        self.play(
            FadeOut(
                electron_gun_rect,
                electron_gun_label,
                lens_sys_rect,
                lens_sys_label,
                sample_rect,
                sample_label,
            )
        )

        self.wait(1)


class EachPart(MovingCameraScene):
    def construct(self):
        self.add(electron_gun_top, electron_gun_bottom, lens, sample_holder)
        self.wait(1)

        # The electron gun shoots electrons
        electron_animations = []
        electron_objs = []
        for i in range(3):
            electron = Dot(UP * 2, radius=0.05, color=C_ELECTRON)
            electron_path = TracedPath(
                electron.get_center,
                stroke_color=C_ELECTRON,
                dissipating_time=0.6,
                stroke_opacity=[1, 0.2, 0],
            )
            delta = 0.5
            electron_line = Line(
                UP * 2, DOWN * 2.5 + LEFT * delta + RIGHT * delta * i
            )  # Invisible

            self.add(electron, electron_path)
            electron_objs.append(electron)
            electron_objs.append(electron_path)
            electron_animations.append(MoveAlongPath(electron, electron_line))

        self.play(FadeIn(electron_gun_rect, electron_gun_label))
        self.play(AnimationGroup(*electron_animations, lag_ratio=0.7))
        self.play(FadeOut(electron_gun_rect, electron_gun_label, *electron_objs))

        self.wait(0.1)

        # 2. we have the lens system
        # The magnetic lens system focuses the electrons to where we want them

        electron_animations = []
        electron_objs = []
        for i in range(5):
            electron = Dot(UP * 2, radius=0.05, color=C_ELECTRON)
            electron_path = TracedPath(
                electron.get_center,
                stroke_color=C_ELECTRON,
                dissipating_time=0.6,
                stroke_opacity=[1, 0.2, 0],
            )
            delta = 0.5
            electron_line = Line(
                UP * 2, LEFT * delta * 2 + RIGHT * delta * i
            )  # Invisible
            delta /= -10
            electron_line.add_line_to(DOWN * 2.5 + LEFT * delta * 2 + RIGHT * delta * i)

            self.add(electron, electron_path)
            electron_objs.append(electron)
            electron_objs.append(electron_path)
            electron_animations.append(MoveAlongPath(electron, electron_line))

        self.play(FadeIn(lens_sys_rect, lens_sys_label), Create(lens_lens))
        self.add(electron, electron_path)
        self.play(AnimationGroup(*electron_animations, lag_ratio=0.3))
        self.wait(0.1)

        # 3. finally we have the sample
        self.play(
            FadeOut(lens_sys_rect, lens_sys_label, lens_lens), FadeOut(*electron_objs)
        )

        electron_detector = Rectangle(height=0.25, width=1.5, **egun_2d_kwargs)
        electron_detector.rotate_about_origin(-75 * DEGREES)
        electron_detector.move_to(RIGHT * 2 + DOWN * 1.5)
        electron_detector_label = Text(
            "Electron Detector", font_size=12, color=C_E_GUN
        ).next_to(electron_detector, DOWN)

        # Maybe move everything to the left and do a zoomed view on the right with details?
        image_to_draw = Square(2.5)
        image_to_draw.move_to(RIGHT * 3 + RIGHT + DOWN)
        image_label = Text("Output image", font_size=12).next_to(image_to_draw, DOWN)
        sample_label_2 = Text("Sample", font_size=12, color=C_SAMPLE).next_to(
            sample_holder, DOWN
        )
        self.play(
            self.camera.frame.animate.move_to(DOWN * 1.5 + RIGHT * 2).set(width=8),
            FadeIn(
                electron_detector, electron_detector_label, image_label, sample_label_2
            ),
            Create(image_to_draw),
        )

        image = [
            [0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
        ]
        C_ZERO = DARK_GRAY
        C_ONE = LIGHTER_GRAY

        grid_objs = [image_to_draw]
        grid_anims = []
        electron_paths = []
        for y, row in enumerate(image):
            for x, val in enumerate(row):
                electron = Dot(UP * 2, radius=0.05, color=C_ELECTRON)
                electron_path = TracedPath(
                    electron.get_center,
                    stroke_color=C_ELECTRON,
                    dissipating_time=1,
                    stroke_opacity=[1, 0.2, 0],
                )
                electron_paths.append(electron_path)
                electron_line = Line(
                    UP * 3,
                    DOWN * 0.5 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x,
                )
                electron_line.add_line_to(DOWN * 2.5 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x)
                self.add(electron_path, electron)
                if val == 1:
                    electron_line.add_line_to(RIGHT * 2 + DOWN * 1.5)
                else:
                    electron_line.add_line_to(
                        DOWN * 2.7 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x
                    )
                square = Square(
                    0.5, fill_opacity=0.7, fill_color=C_ONE if val else C_ZERO
                )
                square.move_to(RIGHT * 3 + RIGHT * x * 0.5 + DOWN * y * 0.5)
                grid_objs += [square, electron, electron_line]
                grid_anims.append(
                    AnimationGroup(
                        [
                            MoveAlongPath(electron, electron_line),
                            FadeIn(square),
                        ],
                        lag_ratio=0.3,
                    ),
                )

        self.play(grid_anims[0], lag_ratio=0.8)
        self.wait(0.5)

        self.play(grid_anims[1], lag_ratio=0.8)
        self.wait(0.5)

        self.play(AnimationGroup(*grid_anims[2:5], lag_ratio=0.8))
        self.wait(1)
        grid_objs = [image_to_draw]
        grid_anims = []
        for y, row in enumerate(image):
            for x, val in enumerate(row):
                electron = Dot(UP * 2, radius=0.05, color=C_ELECTRON)
                electron_path = TracedPath(
                    electron.get_center,
                    stroke_color=C_ELECTRON,
                    dissipating_time=1,
                    stroke_opacity=[1, 0.2, 0],
                )
                electron_line = Line(
                    UP * 3,
                    DOWN * 0.5 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x,
                )
                electron_line.add_line_to(DOWN * 2.5 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x)
                self.add(electron_path, electron)
                if val == 1:
                    electron_line.add_line_to(RIGHT * 2 + DOWN * 1.5)
                else:
                    electron_line.add_line_to(
                        DOWN * 2.7 + LEFT * 0.2 * 2 + RIGHT * 0.2 * x
                    )
                square = Square(
                    0.5, fill_opacity=0.7, fill_color=C_ONE if val else C_ZERO
                )
                square.move_to(RIGHT * 3 + RIGHT * x * 0.5 + DOWN * y * 0.5)
                grid_objs += [square, electron, electron_line]
                grid_anims.append(
                    AnimationGroup(
                        [
                            MoveAlongPath(electron, electron_line),
                            FadeIn(square),
                        ],
                        lag_ratio=0.3,
                    ),
                )

        self.play(AnimationGroup(*grid_anims[5:], lag_ratio=0.2, run_time=5))

        # self.add(electron, electron_path)

        self.wait(1)

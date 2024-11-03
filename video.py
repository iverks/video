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


class Intro(ThreeDScene):
    def construct(self):
        self.move_camera(theta=10 * DEGREES, phi=75 * DEGREES)

        electron_gun_top = Cylinder(
            direction=Z_AXIS,
            checkerboard_colors=[C_E_GUN, C_E_GUN_2],
        )
        electron_gun_bottom = Cone(
            direction=-Z_AXIS,
            checkerboard_colors=[C_E_GUN, C_E_GUN_2],
        )
        electron_gun_top.shift(Z_AXIS * 2)
        electron_gun = VGroup(electron_gun_bottom, electron_gun_top)
        electron_gun.shift(Z_AXIS * 2)

        lens = Cylinder(
            radius=1.5,
            height=1,
            direction=Z_AXIS,
            resolution=(12, 36),
            checkerboard_colors=[C_LENS, C_LENS_2],
        )
        lens.shift(-Z_AXIS * 0)

        sample_holder = Prism(dimensions=[2, 1.8, 0.1], fill_color=C_SAMPLE)
        sample_holder.shift(-Z_AXIS * 2)

        self.play(Create(electron_gun), Create(lens), Create(sample_holder))
        # self.start_rotate_around_z_axis(rate=1) # Kills render speed but looks cool
        self.wait(0.5)

        self.move_camera(theta=0 * DEGREES, phi=90 * DEGREES)

        electron_gun_top_2d = Rectangle(height=2, width=2, **egun_2d_kwargs)
        electron_gun_top_2d.rotate(angle=90 * DEGREES, axis=Y_AXIS)
        electron_gun_top_2d.shift(Z_AXIS * 4)
        electron_gun_bottom_2d = Polygon(
            Z_AXIS * 3 - Y_AXIS, Z_AXIS * 3 + Y_AXIS, Z_AXIS * 2, **egun_2d_kwargs
        )

        lens_2d_l = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
        lens_2d_l.shift(LEFT * 1.5)
        lens_2d_r = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
        lens_2d_r.shift(RIGHT * 1.5)
        lens_2d = VGroup(lens_2d_l, lens_2d_r)
        lens_2d.rotate(angle=90 * DEGREES, axis=Z_AXIS)
        lens_2d.rotate(angle=90 * DEGREES, axis=Y_AXIS)
        lens_2d.shift(Z_AXIS * 0)

        sample_holder_2d = Rectangle(width=2, height=0.1, **sample_2d_kwargs)
        sample_holder_2d.rotate(angle=90 * DEGREES, axis=Z_AXIS)
        sample_holder_2d.rotate(angle=90 * DEGREES, axis=Y_AXIS)
        sample_holder_2d.shift(-Z_AXIS * 2)

        self.play(
            Transform(electron_gun_top, electron_gun_top_2d),
            Transform(electron_gun_bottom, electron_gun_bottom_2d),
            Transform(lens, lens_2d),
            Transform(sample_holder, sample_holder_2d),
        )
        self.wait(2)

    def start_rotate_around_z_axis(self, rate: float = 0.1):
        theta_0 = self.renderer.camera.theta_tracker.get_value()
        val_tracker_theta = ValueTracker(theta_0)

        def update_theta(m, dt):
            val_tracker_theta.increment_value(dt * rate)
            return m.set_value(val_tracker_theta.get_value())

        self.renderer.camera.theta_tracker.add_updater(update_theta)
        self.add(self.renderer.camera.theta_tracker)

    def stop_rotate_around_z_axis(self):
        self.renderer.camera.theta_tracker.clear_updaters()
        self.remove(self.renderer.camera.theta_tracker)


class WorkOverview(Scene):
    def construct(self):
        electron_gun_top = Rectangle(height=2, width=2, **egun_2d_kwargs)
        electron_gun_top.shift(UP * 4)
        electron_gun_bottom = Polygon(
            UP * 3 + LEFT, UP * 3 + RIGHT, UP * 2, **egun_2d_kwargs
        )

        lens_l = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
        lens_l.shift(LEFT * 1.5)
        lens_r = Rectangle(height=1, width=0.2, **lens_2d_kwargs)
        lens_r.shift(RIGHT * 1.5)
        lens = VGroup(lens_l, lens_r)

        sample_holder = Rectangle(width=2, height=0.1, **sample_2d_kwargs)
        sample_holder.shift(DOWN * 2.5)

        self.add(electron_gun_top, electron_gun_bottom, lens, sample_holder)
        self.wait(1)

        # * The electron microscope consists of three main parts
        # The electron gun, the lens system and the sample and sample holder
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
        lens_sys_label = Text(
            "Lens system", font_size=SMALL_FONT_SIZE, color=C_LENS
        ).next_to(lens_sys_rect)

        sample_rect = RoundedRectangle(
            height=1.5,
            width=4,
            corner_radius=0.5,
            stroke_color=C_SAMPLE,
        )
        sample_rect.shift(DOWN * 2.5)
        sample_label = Text(
            "Sample", font_size=SMALL_FONT_SIZE, color=C_SAMPLE
        ).next_to(sample_rect)

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

        # 1. we have the electron gun
        self.play(FadeIn(electron_gun_rect, electron_gun_label))

        self.wait(2)

        self.play(FadeOut(electron_gun_rect, electron_gun_label))

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
            electron_line = Line(
                UP * 2, DOWN * 2.5 + LEFT * 0.1 + RIGHT * 0.1 * i
            )  # Invisible

            self.add(electron, electron_path)
            electron_objs.append(electron)
            electron_objs.append(electron_path)
            electron_animations.append(MoveAlongPath(electron, electron_line))
        self.play(AnimationGroup(*electron_animations, lag_ratio=0.7))
        self.play(FadeOut(*electron_objs))
        self.wait(2)

        # 2. we have the lens system

        self.play(FadeIn(lens_sys_rect, lens_sys_label))

        self.wait(2)

        self.play(FadeOut(lens_sys_rect, lens_sys_label))

        # The magnetic lens system focuses the
        lens_lens = ArcPolygon(
            LEFT * 1.4,
            RIGHT * 1.4,
            radius=4,
            fill_opacity=0.3,
            fill_color=C_LENS,
            stroke_opacity=0.0,
            arc_config={"stroke_width": 1, "stroke_color": C_LENS},
        )
        self.play(Create(lens_lens))

        self.wait(2)

        # TODO: Many electrons
        electron = Dot(UP * 2, radius=0.05, color=C_ELECTRON)
        electron_path = TracedPath(
            electron.get_center,
            stroke_color=C_ELECTRON,
            dissipating_time=0.6,
            stroke_opacity=[1, 0.2, 0],
        )
        electron_line = Line(UP * 2, LEFT * 0.5)  # Invisible
        electron_line.add_line_to(DOWN * 2.5)

        self.add(electron, electron_path)
        self.play(AnimationGroup(MoveAlongPath(electron, electron_line)))
        self.wait(2)

        # 3. finally we have the sample

        self.play(FadeIn(sample_rect, sample_label))

        self.wait(2)

        self.play(FadeOut(sample_rect, sample_label))

        self.wait(1)

        # Maybe move everything to the left and do a zoomed view on the right with details?

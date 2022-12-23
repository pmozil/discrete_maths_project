from manim import *

class Graphx(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (2, 3), (2, 4), (3, 4), (4, 5), (5, 1), (5, 2)]

        graph = Graph(vertices, edges, layout_config={"seed": 0}).scale(1.5)

        self.play(Write(graph))
        self.play(
            graph.vertices[5].animate.shift((LEFT + DOWN) * 0.5),
            graph.vertices[2].animate.shift((RIGHT + DOWN) * 1),
            graph.vertices[1].animate.shift((DOWN) * 0.5))

        self.play(graph.animate.shift(LEFT * 3).scale(5))
        # self.play(graph.animate.shift((DOWN) * 5))
        self.play(graph.vertices[5].animate.set_color(RED))
        self.play(graph.vertices[5].animate.set_color(GREEN))
        self.play(
            graph.vertices[5].animate.set_color(BLUE),
            graph.vertices[4].animate.set_color(RED),
            graph.vertices[3].animate.set_color(GREEN),
            graph.vertices[2].animate.set_color(RED),
            graph.vertices[1].animate.set_color(BLUE)
            )
        # self.play(graph.animate.shift((UP) * 5))
        self.play(graph.animate.scale(0.15))       
        graph2 = graph.copy()
        self.play(
            Write(graph2),
            graph2.animate.shift(RIGHT * 6)
            )
        arrow = Arrow(
            start=graph,
            end=graph2,
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5)
        self.play(
            graph2.vertices[5].animate.set_color(RED),
            graph2.vertices[4].animate.set_color(GREEN),
            graph2.vertices[3].animate.set_color(RED),
            graph2.vertices[2].animate.set_color(BLUE),
            graph2.vertices[1].animate.set_color(GREEN),
            Write(arrow)
            )
        self.wait(1)
        self.play(graph.animate.shift(RIGHT * 3).scale(2), Unwrite(graph2), Unwrite(arrow))
        self.play(
            graph.vertices[5].animate.scale(2),
            graph.vertices[4].animate.scale(2),
            graph.vertices[3].animate.scale(2),
            graph.vertices[2].animate.scale(2),
            graph.vertices[1].animate.scale(2),
            )
        graph3 = Graph(
            vertices,
            edges,
            labels=True,
            layout="circular",
            vertex_config = {1: {"fill_color": BLUE}, 
            2: {"fill_color": RED},
            3: {"fill_color": GREEN},
            4: {"fill_color": RED},
            5: {"fill_color": BLUE},})
        self.play(
            Transform(graph, graph3)
            )
        self.play(graph3.animate.shift(LEFT * 5), graph.animate.shift(LEFT * 5))
        # coords = [(3,2), (2,2), (3,3), (2,3), (3,4), (2,4), (3,5), (2,5), (3,6), (2,6)]
        blue_1 = Text("1", color = BLUE, font="Open Sans").shift(LEFT * 1)
        red_2 = Text("2", color = RED, font="Open Sans").shift(RIGHT * 1)
        # green_3 = Text("3", color = GREEN, font="Open Sans")
        # red_4 = Text("4", color = RED, font="Open Sans")
        # blue_5 = Text("5", color = BLUE, font="Open Sans").shift(RIGHT * 1)
        names_group = VGroup(
            Text("1", color = GREEN, font="Open Sans").shift(UP * 3, RIGHT * 2), 
            Text("1", color = RED, font="Open Sans").shift(UP * 2, RIGHT * 2),
            Text("2", color = BLUE, font="Open Sans").shift(UP * 3, RIGHT * 3),
            Text("2", color = GREEN, font="Open Sans").shift(UP * 2, RIGHT * 3),
            Text("3", color = RED, font="Open Sans").shift(UP * 3, RIGHT * 4),
            Text("3", color = BLUE, font="Open Sans").shift(UP * 2, RIGHT * 4),
            Text("4", color = BLUE, font="Open Sans").shift(UP * 3, RIGHT * 5),
            Text("4", color = GREEN, font="Open Sans").shift(UP * 2, RIGHT * 5),
            Text("5", color = GREEN, font="Open Sans").shift(UP * 3, RIGHT * 6),
            Text("5", color = RED, font="Open Sans").shift(UP * 2, RIGHT * 6)
        )
        green_1 = Text("1", color = GREEN, font="Open Sans")
        red_1 = Text("1", color = RED, font="Open Sans")
        blue_2 = Text("2", color = BLUE, font="Open Sans")
        green_2 = Text("2", color = GREEN, font="Open Sans")
        # red_3 = Text("3", color = RED, font="Open Sans")
        # blue_3 = Text("3", color = BLUE, font="Open Sans")
        # blue_4 = Text("4", color = BLUE, font="Open Sans")
        # green_4 = Text("4", color = GREEN, font="Open Sans")
        # green_5 = Text("5", color = GREEN, font="Open Sans")
        # red_5 = Text("5", color = RED, font="Open Sans")
        self.play(Write(names_group))
        self.play(
            graph3.animate.scale(0.6),
            graph.animate.scale(0.6),
            graph3.animate.to_edge(UL),
            graph.animate.to_edge(UL),
            names_group.animate.scale(0.7)
            )
        arrow0 = Arrow(
            start=blue_1,
            end=red_2,
            max_tip_length_to_length_ratio = 0,
            max_stroke_width_to_length_ratio = 2.5
        ).shift(UP * 0.25)
        self.play(Write(blue_1), Write(red_2), Write(arrow0))
        green_1.shift(DOWN * 1, LEFT * 1)
        red_1.shift(DOWN * 2, LEFT * 1)
        green_2.shift(DOWN * 1, RIGHT * 1)
        blue_2.shift(DOWN * 2, RIGHT * 1)
        self.play(Write(green_1), Write(red_1), Write(green_2), Write(blue_2))
        arrow1 = Arrow(
            start=green_1,
            end=green_2,
            max_tip_length_to_length_ratio = 0,
            max_stroke_width_to_length_ratio = 2.5
            ).set_color(color = [GREEN, WHITE, GREEN]
            ).shift(UP * 0.25)
        arrow2 = Arrow(
            start=green_1,
            end=blue_2,
            max_tip_length_to_length_ratio = 0,
            max_stroke_width_to_length_ratio = 2.5
            ).set_color(color = [BLUE, WHITE, GREEN])
        arrow3 = Arrow(
            start=red_1,
            end=green_2,
            max_tip_length_to_length_ratio = 0,
            max_stroke_width_to_length_ratio = 2.5
            ).set_color(color = [GREEN, WHITE, RED])
        arrow4 = Arrow(
            start=red_1,
            end=blue_2,
            max_tip_length_to_length_ratio = 0,
            max_stroke_width_to_length_ratio = 2.5
            ).set_color(color = [BLUE, WHITE, RED]).shift(UP * 0.25)
        self.play(
            Write(arrow1),
            Write(arrow2),
            Write(arrow3),
            Write(arrow4)
        )
        self.play(Rotate(arrow1, angle = PI/12), runtime = 0.01)
        self.play(Rotate(arrow1, angle = -(PI/6)), runtime = 0.01)
        self.play(Rotate(arrow1, angle = PI/12), runtime = 0.01)
        self.play(Unwrite(arrow1))
        self.play(
            arrow2.animate.shift(LEFT *2),
            arrow3.animate.shift(LEFT *2),
            arrow4.animate.shift(LEFT *2),
            green_1.animate.shift(LEFT *2),
            red_1.animate.shift(LEFT *2),
            blue_2.animate.shift(LEFT *2),
            green_2.animate.shift(LEFT *2)
        )
        separate = Line((0, -0.5, 0), (0, -2.5, 0))
        self.play(Write(separate))
        red_1_copy = red_1.copy().shift(UP * 1, RIGHT * 4)
        blue_2_copy = blue_2.copy().shift(UP * 1, RIGHT * 4)
        orr = Text("or", color = WHITE, font="Open Sans").shift(DOWN * 1, RIGHT * 2)
        self.play(Write(red_1_copy), Write(blue_2_copy), Write(orr))
        green_1_copy = green_1.copy().shift(DOWN * 1, RIGHT * 4)
        green_2_copy = green_2.copy().shift(RIGHT * 4)
        self.play(
            Unwrite(orr),
            Write(green_1_copy),
            Write(green_2_copy),
            blue_2_copy.animate.shift(DOWN * 1)
        )
        implic1 = Arrow(
            end = red_1_copy,
            start = green_2_copy,
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
            ).shift(UP * 0.25)
        implic2 = Arrow(
            start = green_1_copy,
            end = blue_2_copy,
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
            ).shift(UP * 0.25)
        self.play(
            Write(implic1),
            Write(implic2)
            )
        self.play(
            implic1.animate.scale(0.35).shift(UP * 3.2, RIGHT * 1),
            implic2.animate.scale(0.35).shift(UP * 4.8, RIGHT * 1)
        )
        self.play(
            Unwrite(arrow0),
            Unwrite(blue_1),
            Unwrite(red_2),
            Unwrite(green_1),
            Unwrite(green_1_copy),
            Unwrite(green_2),
            Unwrite(green_2_copy),
            Unwrite(red_1),
            Unwrite(red_1_copy),
            Unwrite(blue_2),
            Unwrite(blue_2_copy),
            Unwrite(arrow2),
            Unwrite(arrow3),
            Unwrite(arrow4), 
            Unwrite(separate)
        )
        perform = Text(
            "Perform this for every edge",
            color = WHITE,
            font = "Open Sans"
        ).shift(DOWN * 2, RIGHT * 2)
        self.play(FadeIn(perform))
        self.wait(3)
        self.play(
            graph.animate.shift(LEFT *10),
            graph3.animate.shift(LEFT *10),
            perform.animate.shift(LEFT *15),
            names_group.animate.shift(RIGHT * 10),
            implic1.animate.shift(RIGHT * 10),
            implic2.animate.shift(RIGHT * 10)
        )
        sample_vers = [1, 2, 3]
        edgs = [(1,2), (2,3)]
        sample = Graph(sample_vers, edgs, 
            layout="circular",
            labels = True,
            vertex_config={1: {"fill_color": RED},
            2: {"fill_color": GREEN},
            3: {"fill_color": BLUE}}).shift(LEFT * 5)
        sam_text = Text(
            "Let`s take this graph as an example",
            color = WHITE,
            font = "Open Sans"
        ).shift(RIGHT * 4).scale(0.5)
        self.play(Write(sample), Write(sam_text))
        self.wait(2)
        self.play(Unwrite(sample), Unwrite(sam_text))
        vertices = [10, -10, 12, -12, 21, -21, 22, -22, 30, -30, 31, -31]
        edges = []
        graph_sam2 = Graph(
            vertices, edges,
            layout="circular",
            labels=True,
            vertex_config = {10: {"fill_color": RED},
            -10: {"fill_color": RED},
            12: {"fill_color": GREEN},
            -12: {"fill_color": GREEN},
            21: {"fill_color": GREEN},
            -21: {"fill_color": GREEN},
            22: {"fill_color": BLUE},
            -22: {"fill_color": BLUE},
            30: {"fill_color": RED},
            -30: {"fill_color": RED},
            31: {"fill_color": GREEN},
            -31: {"fill_color": GREEN}}
        ).scale(1.5)
        graph_sam2.vertices[-10].scale(0.65)
        graph_sam2.vertices[-12].scale(0.65)
        graph_sam2.vertices[-21].scale(0.65)
        graph_sam2.vertices[-22].scale(0.65)
        graph_sam2.vertices[-30].scale(0.65)
        graph_sam2.vertices[-31].scale(0.65)
        self.play(Write(graph_sam2))
        arrowm12_10 = Arrow(
            start = graph_sam2.vertices[-12],
            end = graph_sam2.vertices[10],
            max_tip_length_to_length_ratio = 1,
            max_stroke_width_to_length_ratio = 15
        )
        arrow10_m12 = Arrow(
            start = graph_sam2.vertices[10],
            end = graph_sam2.vertices[-12],
            max_tip_length_to_length_ratio = 1,
            max_stroke_width_to_length_ratio = 15
        )
        arrow12_m10 = Arrow(
            start = (1.8, 2.3, 0),
            end = (2.5, 2, 1),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrowm10_12 = Arrow(
            start = (2.5, 2, 1),
            end = (1.8, 2.3, 0),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrow12_m22 = Arrow(
            start = graph_sam2.vertices[12],
            end = graph_sam2.vertices[-22],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        arrow21_m22 = Arrow(
            start = graph_sam2.vertices[21],
            end = graph_sam2.vertices[-22],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        arrowm21_22 = Arrow(
            start = (-2.6,1, 0),
            end = (-2.8,0.4, 1),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrow22_m21 = Arrow(
            start = (-2.8,0.4, 1),
            end = (-2.6,1, 0),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrowm22_21 = Arrow(
            start = graph_sam2.vertices[-22],
            end = graph_sam2.vertices[21],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        arrow21_m31 = Arrow(
            start = graph_sam2.vertices[21],
            end = graph_sam2.vertices[-31],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        arrowm30_31 = Arrow(
            end = (1, -2.8, 0),
            start = (0.5, -3, 1),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrowm31_30 = Arrow(
            start = graph_sam2.vertices[-31],
            end = graph_sam2.vertices[30],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        arrow30_m31 = Arrow(
            start = graph_sam2.vertices[30],
            end = graph_sam2.vertices[-31],
            max_tip_length_to_length_ratio = 0.5,
            max_stroke_width_to_length_ratio = 10
        )
        arrow31_m30 = Arrow(
            start = (1, -2.8, 0),
            end = (0.5, -3, 1),
            max_tip_length_to_length_ratio = 0.3,
            max_stroke_width_to_length_ratio = 4
        )
        arrow31_m21 = Arrow(
            start = graph_sam2.vertices[-31],
            end = graph_sam2.vertices[21],
            max_tip_length_to_length_ratio = 0.1,
            max_stroke_width_to_length_ratio = 2.5
        )
        self.play(
            Write(arrow10_m12),
            Write(arrowm12_10), Write(arrow12_m10),
            Write(arrowm10_12), Write(arrow12_m22),
            Write(arrow21_m22), Write(arrowm21_22), Write(arrow22_m21),
            Write(arrowm22_21), Write(arrow21_m31),
            Write(arrowm30_31), Write(arrowm31_30),
            Write(arrow30_m31), Write(arrow31_m30),
            Write(arrow31_m21))
        self.wait(1)
        self.play(
            graph_sam2.vertices[-10].animate.set_color(PINK),
            graph_sam2.vertices[12].animate.set_color(PINK),
            graph_sam2.vertices[21].animate.set_color(PURPLE),
            graph_sam2.vertices[-22].animate.set_color(PURPLE),
            graph_sam2.vertices[-31].animate.set_color(PURPLE),
            graph_sam2.vertices[-30].animate.set_color(PURPLE),
            graph_sam2.vertices[10].animate.set_color(YELLOW),
            graph_sam2.vertices[-12].animate.set_color(YELLOW),
            graph_sam2.vertices[22].animate.set_color(YELLOW),
            graph_sam2.vertices[-21].animate.set_color(YELLOW),
            graph_sam2.vertices[31].animate.set_color(YELLOW),
            graph_sam2.vertices[-30].animate.set_color(YELLOW),
            graph_sam2.vertices[30].animate.set_color(WHITE)
            )
        self.wait(30)
        self.play(
            Unwrite(arrow10_m12),
            Unwrite(arrowm12_10), Unwrite(arrow12_m10),
            Unwrite(arrowm10_12), Unwrite(arrow12_m22),
            Unwrite(arrow21_m22), Unwrite(arrowm21_22), Unwrite(arrow22_m21),
            Unwrite(arrowm22_21), Unwrite(arrow21_m31),
            Unwrite(arrowm30_31), Unwrite(arrowm31_30),
            Unwrite(arrow30_m31), Unwrite(arrow31_m30),
            Unwrite(arrow31_m21), Unwrite(graph_sam2))

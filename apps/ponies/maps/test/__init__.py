from core.map import MapType, Map

class TestMap(MapType):

    def load(self):
        map = Map()

        map.set_background(image.load("/system/apps/ponies/maps/test/background.png"))

        graph = GraphBuilder()

        # Spawn
        graph.node(SpawnNode(0, 369, 88))

        # Loop around blanket
        graph.node(PathNode(1, 369, 127)).link([0])
        graph.node(PathNode(2, 504, 165)).link([1])
        graph.node(PathNode(3, 542, 212)).link([2])
        graph.node(PathNode(4, 526, 290)).link([3])
        graph.node(PathNode(5, 456, 328)).link([4])
        graph.node(PathNode(6, 369, 356)).link([5])
        graph.node(PathNode(7, 292, 325)).link([6])
        graph.node(PathNode(8, 212, 273)).link([7])
        graph.node(PathNode(9, 208, 192)).link([8])
        graph.node(PathNode(10, 256, 157)).link([9, 0])

        # Path to castle
        graph.node(PathNode(11, 372, 439)).link([6])
        graph.node(PathNode(12, 331, 508)).link([11])
        graph.node(PathNode(13, 258, 541)).link([12])
        graph.node(PathNode(14, 145, 541)).link([13])
        graph.node(PathNode(15, 145, 487)).link([14])
        graph.node(ActivityAreaNode(16, 68, 364, 152, 125)).link([15])

        # Bench
        graph.node(PathNode(17, 176, 150)).link([9, 10])
        graph.node(ActivityNode(18, 158, 117)).link([17])
        graph.node(ActivityNode(19, 194, 117)).link([17, 18])

        map.graph = graph.build()

        return map
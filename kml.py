from pykml import parser
import simplekml


class KML:

    def take_coordinates_from_kml_file(file):
        f = open(file)
        data = parser.parse(f).getroot()
        mass = str(data.Document.Placemark.LineString.coordinates).split()
        coordinates = []
        for value in mass:
            coordinates.append(list(map(lambda x: float(x), value.split(','))))
        f.close()
        return coordinates

    def write_coordinates_to_kml_file(crds_1, crds_2, file, color1, color2):
        f = simplekml.Kml()
        line1 = f.newlinestring(tessellate="1", coords=[x for x in crds_1])
        line2 = f.newlinestring(tessellate="2", coords=[x for x in crds_2])
        line1.style.linestyle.color = color1
        line2.style.linestyle.color = color2
        f.save(f'{file}')

    def choose_color(object):
        print(f"choose the color of the {object} trajectory")
        flag = input("1 Blue \n2 White \n3 Black \n4 Red \n5 Yellow \n ")
        match flag:
            case "1":
                color = simplekml.Color.blue
            case "2":
                color = simplekml.Color.white
            case "3":
                color = simplekml.Color.black
            case "4":
                color = simplekml.Color.red
            case "5":
                color = simplekml.Color.yellow

        return color

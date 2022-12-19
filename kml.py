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

    def write_coordinates_to_kml_file(massiv_s_coord, file):
        f = simplekml.Kml()
        f.newlinestring(tessellate="uiyf", coords=[x for x in massiv_s_coord])
        f.save(f'{file}')

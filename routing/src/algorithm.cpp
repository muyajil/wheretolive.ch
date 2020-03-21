#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <limits>
#include <stdexcept>

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Delaunay_triangulation_2.h>

using namespace std;

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Delaunay_triangulation_2<K> Triangulation;

typedef std::map<K::Point_2, string> CoordinatesToIdMap;

/**
 * Read in stations, build triangulation and return it. Used for nearest post office problem.
 */
Triangulation buildTriangulation(CoordinatesToIdMap &coToIdMap, std::size_t numberStations) {
  // read points
  std::vector<K::Point_2> pts;
  pts.reserve(numberStations);
  std::map<K::Point_2, string> testMap;
  for (std::size_t i = 0; i < numberStations; ++i) {
    string name;
    double x, y;
    std::cin >> name >> x >> y;
    K::Point_2 p = K::Point_2(x, y);
    coToIdMap[p] = name;
    pts.push_back(p);
  }
  // construct triangulation
  Triangulation t;
  t.insert(pts.begin(), pts.end());

  return t;
}

string nearestStation(K::Point_2 &point, Triangulation &t, CoordinatesToIdMap &stationNames) {
  Triangulation::Vertex_handle p = t.nearest_vertex(point);
  return stationNames[p->point()];
}

void handleInput() {
  int n;
  std::cin >> n;
  
  CoordinatesToIdMap coToIdMap;
  Triangulation t = buildTriangulation(coToIdMap, n);

  int m;
  std::cin >> m;
  for (int i = 0; i < m; i++) {
    string name;
    double x, y;
    std::cin >> name >> x >> y;
    
    K::Point_2 p = K::Point_2(x, y);
    string stationId = nearestStation(p, t, coToIdMap);
    std::cout << stationId << std::endl;
  }
}

int main(int argc, char const *argv[]) {
  ios_base::sync_with_stdio(false);
  handleInput();
  return 0;
}
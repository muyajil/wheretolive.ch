package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"runtime"
	"strconv"
)

var transferMap map[string]map[string]int
var stationGroups map[string]map[string]int
var connections []connection
var commutes []commute

type journey struct {
	time    int
	changes int
}

func isTransferDestPossible(connection connection, eA *map[string]int) bool {
	arrivalTime, exists := (*eA)[connection.toStopID]
	if !exists {
		return true
	}
	return connection.arrivalTime < arrivalTime
}

func isTransferOriginPossible(connection connection, eA *map[string]int, iC *map[string]connection) bool {
	_, exists := (*eA)[connection.fromStopID]
	if !exists {
		return false
	}

	prevConnection, exists := (*iC)[connection.fromStopID]

	if !exists {
		return true
	}

	transfers, exists := transferMap[prevConnection.exactToStopID]

	if !exists {
		return prevConnection.arrivalTime <= connection.departureTime
	}

	transferTime, exists := transfers[connection.exactFromStopID]

	if !exists {
		return prevConnection.arrivalTime <= connection.departureTime
	}

	return prevConnection.arrivalTime+transferTime <= connection.departureTime

}

func computeRoute(commute commute, iC *map[string]connection) []connection {
	route := make([]connection, 0)

	if _, exists := (*iC)[commute.target]; !exists {
		return route
	}

	lastStopID := commute.target
	possibleDepartureStopIDs := []string{commute.source}

	if stationGroup, exists := stationGroups[commute.source]; exists {
		for stationID := range stationGroup {
			possibleDepartureStopIDs = append(possibleDepartureStopIDs, stationID)
		}
	}

	arrived := false

	for !arrived {
		lastConnection := (*iC)[lastStopID]
		route = append(route, lastConnection)
		lastStopID = lastConnection.fromStopID
		for _, possibleDepartureStopID := range possibleDepartureStopIDs {
			if lastStopID == possibleDepartureStopID {
				arrived = true
			}
		}
	}

	return route
}

func computeCSA(target string, eA *map[string]int, iC *map[string]connection) {
	earliest := math.MaxInt32

	for _, c := range connections {
		if isTransferDestPossible(c, eA) && isTransferOriginPossible(c, eA, iC) {
			(*eA)[c.toStopID] = c.arrivalTime
			(*iC)[c.toStopID] = c

			if stationGroup, exists := stationGroups[c.toStopID]; exists {
				for stationID, walkingTime := range stationGroup {
					potentialArrivalTime := c.arrivalTime + walkingTime

					if arrivalTime, exists := (*eA)[stationID]; !exists || arrivalTime > potentialArrivalTime {
						(*eA)[stationID] = potentialArrivalTime
						(*iC)[stationID] = connection{
							fromStopID:      c.toStopID,
							exactFromStopID: c.toStopID,
							toStopID:        stationID,
							exactToStopID:   stationID,
							departureTime:   c.arrivalTime,
							arrivalTime:     (*eA)[stationID],
							tripID:          ""}
					}
				}
			}

			if arrivalTime, exists := (*eA)[target]; exists {
				earliest = arrivalTime
			}
		}

		if c.arrivalTime > earliest {
			return
		}
	}
}

func computeJourney(commute commute, eA *map[string]int, iC *map[string]connection) journey {

	if commute.source == commute.target {
		return journey{
			time:    0,
			changes: 0}
	}

	(*eA)[commute.source] = 6 * 3600

	if stationGroup, exists := stationGroups[commute.source]; exists {
		for stationID, walkingTime := range stationGroup {
			(*eA)[stationID] = (*eA)[commute.source] + walkingTime
		}
	}

	computeCSA(commute.target, eA, iC)
	route := computeRoute(commute, iC)

	if len(route) == 0 {
		return journey{
			time:    -1,
			changes: -1}
	}

	time := route[0].arrivalTime - route[len(route)-1].departureTime
	tripIDs := make(map[string]bool, 0)
	for _, connection := range route {
		if connection.tripID != "" {
			tripIDs[connection.tripID] = true
		}
	}

	return journey{
		time:    time,
		changes: len(tripIDs) - 1}
}

func worker(jobs <-chan commute, results chan<- []string) {
	for c := range jobs {
		earliestArrival := make(map[string]int)
		inConnection := make(map[string]connection)
		j := computeJourney(c, &earliestArrival, &inConnection)
		results <- []string{c.source, c.target, c.commuteType, strconv.Itoa(j.time), strconv.Itoa(j.changes)}
	}
}

func csvWriter(results <-chan []string, finished chan<- bool) {
	file, err := os.Create("/tmp/train_commutes.csv")
	if err != nil {
		fmt.Print(err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)

	for result := range results {
		writer.Write(result)
		if err != nil {
			fmt.Print(err)
		}
	}
	writer.Flush()
	file.WriteString("done")
	finished <- true
}

func main() {
	transferMap = getTransferMap()
	fmt.Println("Loaded Transfer Map")
	stationGroups = getStationGroups()
	fmt.Println("Loaded Station Groups")
	connections = getConnections()
	fmt.Println("Loaded Connections")
	commutes = getCommutes()
	fmt.Println("Loaded Commutes")

	numWorkers := runtime.NumCPU() - 4

	jobs := make(chan commute, numWorkers)
	results := make(chan []string, numWorkers)
	finished := make(chan bool)

	for w := 1; w <= numWorkers; w++ {
		go worker(jobs, results)
	}
	go csvWriter(results, finished)

	for _, c := range commutes {
		jobs <- c
	}
	close(jobs)
	fmt.Println("Sent all jobs")
	<-finished
	fmt.Println("Finished all jobs")
}

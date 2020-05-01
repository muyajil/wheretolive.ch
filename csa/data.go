package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strconv"
)

type connection struct {
	fromStopID      string
	exactFromStopID string
	toStopID        string
	exactToStopID   string
	departureTime   int
	arrivalTime     int
	tripID          string
}

type commute struct {
	source      string
	target      string
	commuteType string
}

func getTransferMap() map[string]map[string]int {
	data, err := ioutil.ReadFile("/tmp/transfer_map.json")
	if err != nil {
		fmt.Print(err)
	}

	var transferMap map[string]map[string]int
	json.Unmarshal(data, &transferMap)
	return transferMap
}

func getStationGroups() map[string]map[string]int {
	data, err := ioutil.ReadFile("/tmp/station_groups.json")
	if err != nil {
		fmt.Print(err)
	}

	var stationGroups map[string]map[string]int
	json.Unmarshal(data, &stationGroups)
	return stationGroups
}

func getConnections() []connection {
	csvFile, _ := os.Open("/tmp/connections.csv")
	reader := csv.NewReader(bufio.NewReader(csvFile))
	var connections []connection
	for {
		line, error := reader.Read()
		if error == io.EOF {
			break
		} else if error != nil {
			log.Fatal(error)
		}
		departureTime, _ := strconv.Atoi(line[4])
		arrivalTime, _ := strconv.Atoi(line[5])
		connections = append(connections, connection{
			fromStopID:      line[0],
			exactFromStopID: line[1],
			toStopID:        line[2],
			exactToStopID:   line[3],
			departureTime:   departureTime,
			arrivalTime:     arrivalTime,
			tripID:          line[6]})
	}

	return connections
}

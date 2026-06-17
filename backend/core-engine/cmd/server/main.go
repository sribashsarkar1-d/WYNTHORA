package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Starting Core Engine (Go) on port 8080...")
	http.HandleFunc("/api/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Core Engine is running"))
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}

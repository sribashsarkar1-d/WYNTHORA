package api
import "net/http"
func RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("/api/v1/simulate", func(w http.ResponseWriter, r *http.Request) { w.Write([]byte("Simulate")) })
}

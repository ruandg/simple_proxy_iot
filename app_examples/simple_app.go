package main
import (
    "net"
    "os"
)

func main() {
    args := os.Args[1:]

    if(len(args) != 2){
        println("usage: simple_app.go SERVER_ADDRESS_OR_URL PORT")
        return;
    }

    addr := args[0]
    port := args[1]

    servAddr := addr+":"+port

    tcpAddr, err := net.ResolveTCPAddr("tcp", servAddr)
    if err != nil {
        println("ResolveTCPAddr failed:", err.Error())
        os.Exit(1)
    }

    conn, err := net.DialTCP("tcp", nil, tcpAddr)
    if err != nil {
        println("Dial failed:", err.Error())
        os.Exit(1)
    }
    data := "app"
    _, err = conn.Write([]byte(data))
    if err != nil {
        println("Write to server failed:", err.Error())
        os.Exit(1)
    }

    reply := make([]byte, 1024)

    _, err = conn.Read(reply)
    if err != nil {
        println("Reade from server failed:", err.Error())
        os.Exit(1)
    }

    println(string(reply))
   
    data = "123456789"

    _, err = conn.Write([]byte(data))
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }

    _, err = conn.Read(reply)
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }

    println(string(reply))

    _, err = conn.Read(reply)
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }

    println("Dado recebido: ", string(reply))

    conn.Close()
}
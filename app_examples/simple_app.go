package main
import (
    "net"
    "os"
)

func main() {
    args := os.Args[1:]

    if(len(args) != 3){
        println("usage: simple_app.go SERVER_ADDRESS_OR_URL PORT DEVICE_ID")
        return;
    }

    addr := args[0]
    port := args[1]
    device_id := args[2]

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
    nbytes := 0

    nbytes, err = conn.Read(reply)
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }
   
    sreply := string(reply[:nbytes])
    println(sreply)

    if(sreply == "fail") {
        conn.Close()
        os.Exit(1)
    }
   
    data = device_id

    _, err = conn.Write([]byte(data))
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }

    nbytes, err = conn.Read(reply)
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }
    
    sreply = string(reply[:nbytes])
    println(sreply)

    if(sreply == "fail") {
        conn.Close()
        os.Exit(1)
    }

    nbytes, err = conn.Read(reply)
    if err != nil {
        println("Read from server failed:", err.Error())
        os.Exit(1)
    }
    reply[nbytes] = 0 //character indicating the end of the string

    println("Dado recebido: ", string(reply))

    conn.Close()
}
package com.jetbrains

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.*
import io.ktor.server.request.receive
import io.ktor.server.request.receiveText
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Application.configureRouting() {
    routing {
        get("/") {
            call.respondText("KTOR(v 2.2.4) Vulnerable app - CVE-2023-45612")
        }
        post("/xml") {
            try {
                println("Received request, attempting to parse...")
                val message = call.receive<Message>()
                println("Successfully parsed: $message")
                call.respondText("Received message: ${message.text}")
            } catch (e: Exception) {
                println("Error: ${e.message}")
                e.printStackTrace()
                call.respondText("Error: ${e.message}", status = HttpStatusCode.BadRequest)
            }
        }
    }
}

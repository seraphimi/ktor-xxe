package com.jetbrains

import io.ktor.serialization.kotlinx.xml.xml
import io.ktor.server.application.*
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation

fun main(args: Array<String>) {
    io.ktor.server.netty.EngineMain.main(args)
}

fun Application.module() {
        install(ContentNegotiation) {
      xml()
    }
    configureRouting()
}

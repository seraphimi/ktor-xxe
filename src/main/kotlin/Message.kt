package com.jetbrains

import kotlinx.serialization.Serializable
import nl.adaptivity.xmlutil.serialization.XmlElement
import nl.adaptivity.xmlutil.serialization.XmlSerialName

@Serializable
@XmlSerialName("Message", "", "")
data class Message(
    @XmlElement(true)
    val text: String = "",
)
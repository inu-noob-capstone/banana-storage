package com.example.leavemealoneapplication

import android.content.SharedPreferences
import android.renderscript.ScriptGroup
import android.widget.TextView

class MainActivityUpdateAsSettingFile(var shared:SharedPreferences, val TextView1:android.widget.TextView):Runnable {
    override fun run() {
        val currentLuxMessage = "현재 조도 : " + shared.getString("currentLux", "기본값") +" Lux"
        TextView1.text = currentLuxMessage
    }
}
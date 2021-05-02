package com.example.leavemealoneapplication

import android.content.SharedPreferences
import android.util.Log
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.lang.StringBuilder
import java.net.HttpURLConnection
import java.net.URL
import java.util.logging.Handler

class SettingFileUpdate(var shared: SharedPreferences, var mainActivityUpdate: android.os.Handler,
                        val mHandler: Handler): Runnable {
    override fun run() {

        var lightUrlText = "http://192.168.219.110/lightSetting.json"
        var waterUrlText = "http://192.168.219.110/waterSetting.json"

        val lightUrl = URL(lightUrlText)
        val waterUrl = URL(waterUrlText)

        val lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
        val waterUrlConnection = waterUrl.openConnection() as HttpURLConnection

        lightUrlConnection.requestMethod = "GET"
        waterUrlConnection.requestMethod = "GET"

        if(lightUrlConnection.responseCode == HttpURLConnection.HTTP_OK){
            val streamReader = InputStreamReader(lightUrlConnection.inputStream)
            val buffered = BufferedReader(streamReader)

            val content = StringBuilder()
            while(true){
                val line = buffered.readLine()?: break
                content.append(line)
            }

            var lightJson = JSONObject(content.toString())
            var currentLux = lightJson.get("currentLux")
            Log.d("AAA","${currentLux}")

            val editor = shared.edit()
            editor.putString("currentLux", "${currentLux}")
            editor.apply()
        }
    }
}
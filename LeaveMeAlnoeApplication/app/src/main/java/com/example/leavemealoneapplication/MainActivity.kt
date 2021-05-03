package com.example.leavemealoneapplication

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.JsonReader
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.example.leavemealoneapplication.databinding.ActivityMainBinding
import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader
import java.lang.StringBuilder
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread


class MainActivity : AppCompatActivity() {
    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        suspend fun updateUI(currentLuxMessage:String, humidityMessage:String){
            binding.mainCurrentLux.text = currentLuxMessage
            binding.mainCurrentHumidity.text = humidityMessage
        }

        val sharedLight = getSharedPreferences("lightSetting", Context.MODE_PRIVATE)
        val sharedWater = getSharedPreferences("waterSetting", Context.MODE_PRIVATE)

        val lightEditor = sharedLight.edit()
        val waterEditor = sharedWater.edit()



        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                if (isWiFiAvailable(applicationContext)) {
                    var lightUrlText = "http://192.168.219.110/lightSetting.json"
                    var waterUrlText = "http://192.168.219.110/waterSetting.json"

                    var lightUrl = URL(lightUrlText)
                    var waterUrl = URL(waterUrlText)

                    var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
                    lightUrlConnection.requestMethod = "GET"
                    lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

                    var waterUrlConnection = waterUrl.openConnection() as HttpURLConnection
                    waterUrlConnection.requestMethod = "GET"
                    waterUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

                    var response = lightUrlConnection.responseCode
                    Log.d("response==", response.toString())

                    var response2 = waterUrlConnection.responseCode
                    Log.d("response==", response.toString())

                    var lightInputStream = lightUrlConnection.getInputStream()
                    var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    var lightContent = lightBuffered.readText()

                    var waterInputStream = waterUrlConnection.getInputStream()
                    var waterBuffered = BufferedReader(InputStreamReader(waterInputStream, "UTF=8"))
                    var waterContent = waterBuffered.readText()

                    Log.d("lightResponse", "Size: " + lightContent.length)
                    Log.d("waterResponse", "Size: " + waterContent.length)
                    //Log.d("content", "${lightContent}")

                    fun safeLightCall(lightContent: String?): String? {
                        if ((lightContent != null) && (lightContent.length !== 0)) {
                            var lightJson = JSONObject(lightContent)
                            var currentLux = "${lightJson.get("currentLux")}"
                            return currentLux
                        } else {
                            return null
                        }
                    }

                    var currentLux: String? = safeLightCall(lightContent)
                    var currentLuxMessage: String?
                    currentLuxMessage = null
                    if (currentLux != null) {
                        currentLuxMessage = "현재 조도 : " + currentLux + " Lux"
                    }

                    fun safeWaterCall(waterContent: String?): String? {
                        if ((waterContent != null) && (waterContent.length != 0)) {
                            var waterJson = JSONObject(waterContent)
                            var humidity = "${waterJson.get("humidity")}"
                            return humidity
                        } else {
                            return null
                        }
                    }

                    var humidity: String? = safeWaterCall(waterContent)
                    var humidityMessage: String?
                    humidityMessage = null
                    if (humidity != null) {
                        humidityMessage = "현재 습도 : " + humidity + "%"
                    }

                    if ((currentLuxMessage != null) && (humidityMessage != null)) {
                        withContext(Dispatchers.Main) {
                            updateUI(currentLuxMessage, humidityMessage)
                        }
                    }

                    lightEditor.putString("currentLux", "${currentLux}")
                    lightEditor.apply()
                    waterEditor.putString("humidity", "${humidity}")
                    waterEditor.apply()

                    lightBuffered.close()
                    waterBuffered.close()

                    lightUrlConnection.disconnect()
                    waterUrlConnection.disconnect()

                    delay(850L)
                } else {
                    var currentLux = sharedLight.getString("currentLux", "기본값")
                    var humidity = sharedWater.getString("humidity", "기본값")

                    var currentLuxMessage = "현재 조도 : " + currentLux + " Lux"
                    var humidityMessage = "현재 습도 : " + humidity + "%"

                    withContext(Dispatchers.Main) {
                        binding.mainCurrentLux.text = currentLuxMessage
                        binding.mainCurrentHumidity.text = humidityMessage
                    }
                }
            }
        }

        //val editor = shared.edit()
        //editor.putString("currentLux", "258")
        //editor.apply()

        //val currentLuxMessage = "현재 조도 : " + shared.getString("currentLux", "기본값") +" Lux"
        //binding.mainCurrentLux.text = currentLuxMessage

        val moistureIntent = Intent(this, MoistureManagement::class.java)
        val lightIntent = Intent(this, LightManagement::class.java)
        val communicationIntent = Intent(this, Communication::class.java)

        binding.mainMoisture.setOnClickListener { startActivity(moistureIntent) }
        binding.mainLight.setOnClickListener { startActivity(lightIntent) }
        binding.mainCommunication.setOnClickListener { startActivity(communicationIntent) }
    }
}

package com.example.leavemealoneapplication

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.JsonToken
import android.util.Log
import androidx.annotation.IdRes
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import com.example.leavemealoneapplication.databinding.ActivityMainBinding
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import kotlinx.coroutines.*
import nl.bryanderidder.themedtogglebuttongroup.ThemedButton
import nl.bryanderidder.themedtogglebuttongroup.ThemedToggleButtonGroup
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import retrofit2.Retrofit
import retrofit2.create
import java.io.*
import java.net.HttpURLConnection
import java.net.URL
import kotlin.text.Typography.less

class LightManagement : AppCompatActivity() {
    val binding by lazy { ActivityLightManagementBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        var sharedLight = getSharedPreferences("lightSetting", Context.MODE_PRIVATE)
        var lightEditor = sharedLight.edit()

        CoroutineScope(Dispatchers.IO).launch {
            var lightUrlText = "http://192.168.219.110/lightSetting.json"
            var lightUrl = URL(lightUrlText)

            var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            var lightInputStream = lightUrlConnection.getInputStream()
            var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
            var lightContent = lightBuffered.readText()

            Log.d("lightResponse", "Size: " + lightContent.length)

            while (true) {
                if ((lightContent != null) && (lightContent.length != 0)) {
                    var lightJson = JSONObject(lightContent)

                    var goalLux = "${lightJson.get("goalLux")}"
                    lightEditor.putString("goalLux", "${goalLux}")
                    lightEditor.apply()

                    var chlorophyll = "${lightJson.get("chlorophyll")}"
                    lightEditor.putString("chlorophyll", "${chlorophyll}")
                    lightEditor.apply()

                    var allowingOfAUser = "${lightJson.get("allowingOfAUser")}"
                    lightEditor.putString("allowingOfAUser", "${allowingOfAUser}")
                    lightEditor.apply()

                    break
                } else {
                    lightUrlConnection.disconnect()
                    lightBuffered.close()

                    lightInputStream = lightUrlConnection.getInputStream()
                    lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    lightContent = lightBuffered.readText()
                }
            }

            var goalLux = sharedLight.getString("goalLux", "0")
            var chlorophyll = sharedLight.getString("chlorophyll", "A")
            var allowingOfAUser = sharedLight.getString("allowingOfAUser", "true")

            withContext(Dispatchers.Main) {
                binding.currentLuxGoalText.text = "${goalLux}" + " Lux"

                if (chlorophyll == "A") {
                    binding.chlorophyllBButton.selectButton(binding.less.id)
                } else if (chlorophyll == "B") {
                    binding.chlorophyllBButton.selectButton(binding.normal.id)
                } else {
                    binding.chlorophyllBButton.selectButton(binding.lots.id)
                }

                if (allowingOfAUser == "true") {
                    binding.lightOnOffToggleBtn.check(binding.on.id)
                } else {
                    binding.lightOnOffToggleBtn.check(binding.off.id)
                }
            }
        }

        binding.saveSetting.setOnClickListener {

            if (binding.editGoalLux.text.toString().length != 0) {
                lightEditor.putString("goalLux", binding.editGoalLux.text.toString())
                lightEditor.apply()
                Log.d("lightUpdate", "goalLux : " + "${binding.editGoalLux.text.toString()}")
            }

            if (binding.less.isSelected == true) {
                lightEditor.putString("chlorophyll", "A")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : A")
            } else if (binding.normal.isSelected == true) {
                lightEditor.putString("chlorophyll", "B")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : B")
            } else {
                lightEditor.putString("chlorophyll", "C")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : C")
            }

            if (binding.on.id == binding.lightOnOffToggleBtn.checkedId) {
                lightEditor.putString("allowingOfAUser", "true")
                lightEditor.apply()
                Log.d("lightUpdate", "allowingOfAUser : true")
            } else if (binding.off.id == binding.lightOnOffToggleBtn.checkedId) {
                lightEditor.putString("allowingOfAUser", "false")
                lightEditor.apply()
                Log.d("lightUpdate", "allowingOfAUser : false")
            }

            // 아래부턴 goalLux 데이터 전송

            var goalLux = sharedLight.getString("goalLux", "0")

            var lightUrlText = "http://192.168.219.110:8081/?goalLux=" + "${goalLux}"
            var lightUrl = URL(lightUrlText)

            var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            CoroutineScope(Dispatchers.IO).launch {
                while(true) {
                    var lightInputStream = lightUrlConnection.getInputStream()
                    var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    var lightContent = lightBuffered.readText()

                    if ((lightContent != null) && (lightContent.length != 0)) {
                        break
                    } else {
                        lightUrlConnection.disconnect()
                        lightBuffered.close()

                        lightInputStream = lightUrlConnection.getInputStream()
                        lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                        lightContent = lightBuffered.readText()
                    }
                }
            }

            // 아래부터 엽록소 데이터 전송

            var chlorophyll = sharedLight.getString("chlorophyll","A")

            lightUrlText = "http://192.168.219.110:8081/?chlorophyll=" + "${chlorophyll}"
            lightUrl = URL(lightUrlText)

            lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            CoroutineScope(Dispatchers.IO).launch {
                while(true) {
                    var lightInputStream = lightUrlConnection.getInputStream()
                    var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    var lightContent = lightBuffered.readText()

                    if ((lightContent != null) && (lightContent.length != 0)){
                        break
                    } else{
                        lightUrlConnection.disconnect()
                        lightBuffered.close()

                        lightInputStream = lightUrlConnection.getInputStream()
                        lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                        lightContent = lightBuffered.readText()
                    }
                }
            }

            // 아래부터 allowingOfAUser(전구 강제로 끄기) 데이터 전송

            var allowingOfAUser = sharedLight.getString("allowingOfAUser","true")

            lightUrlText = "http://192.168.219.110:8081/?allowingOfAUser=" + "${allowingOfAUser}"
            lightUrl = URL(lightUrlText)

            lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            CoroutineScope(Dispatchers.IO).launch {
                while(true) {
                    var lightInputStream = lightUrlConnection.getInputStream()
                    var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    var lightContent = lightBuffered.readText()

                    if ((lightContent != null) && (lightContent.length != 0)){
                        break
                    } else{
                        lightUrlConnection.disconnect()
                        lightBuffered.close()

                        lightInputStream = lightUrlConnection.getInputStream()
                        lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                        lightContent = lightBuffered.readText()
                    }
                }
            }

            finish() // 현 액티비티 종료
            //val MainIntent = Intent(this, MainActivity::class.java)
            //startActivity(MainIntent)
            //finish()
            //recreate()
            //recreate()

        } // 버튼 onClickListener 블록 끝

    }
}
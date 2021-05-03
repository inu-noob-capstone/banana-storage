package com.example.leavemealoneapplication

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.annotation.IdRes
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import com.example.leavemealoneapplication.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import kotlin.text.Typography.less

class LightManagement : AppCompatActivity() {
    val binding by lazy { ActivityLightManagementBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        val sharedLight = getSharedPreferences("lightSetting", Context.MODE_PRIVATE)
        val lightEditor = sharedLight.edit()

        CoroutineScope(Dispatchers.IO).launch{
            var lightUrlText = "http://192.168.219.110/lightSetting.json"
            var lightUrl = URL(lightUrlText)

            var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            var lightInputStream = lightUrlConnection.getInputStream()
            var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
            var lightContent = lightBuffered.readText()

            Log.d("lightResponse", "Size: "+lightContent.length)

            while(true) {
                if ((lightContent != null) && (lightContent.length != 0)) {
                    var lightJson = JSONObject(lightContent)

                    var goalLux = "${lightJson.get("goalLux")}"
                    lightEditor.putString("goalLux", "${goalLux}")
                    lightEditor.apply()

                    var chlorophyll = "${lightJson.get("chlorophyll")}"
                    lightEditor.putString("chlorophyll", "${chlorophyll}")
                    lightEditor.apply()

                    var allowingOfAUser = "${lightJson.get("allowingOfAUser")}"
                    lightEditor.putString("allowingOfAUser","${allowingOfAUser}")
                    lightEditor.apply()

                    break
                }
                else{
                    lightUrlConnection.disconnect()
                    lightBuffered.close()

                    lightInputStream = lightUrlConnection.getInputStream()
                    lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    lightContent = lightBuffered.readText()
                }
            }

            var goalLux = sharedLight.getString("goalLux","0")
            var chlorophyll = sharedLight.getString("chlorophyll", "A")
            var allowingOfAUser = sharedLight.getString("allowingOfAUser", "true")

            withContext(Dispatchers.Main){
                binding.currentLuxGoalText.text = "${goalLux}"+" Lux"

                if (chlorophyll == "A"){
                    binding.chlorophyllBButton.selectButton(binding.less.id)
                }
                else if (chlorophyll == "B"){
                    binding.chlorophyllBButton.selectButton(binding.normal.id)
                }
                else{
                    binding.chlorophyllBButton.selectButton(binding.lots.id)
                }

                if (allowingOfAUser == "true"){
                    binding.lightOnOffToggleBtn.check(binding.on.id)
                }
                else{
                    binding.lightOnOffToggleBtn.check(binding.off.id)
                }
            }


        }
    }
}
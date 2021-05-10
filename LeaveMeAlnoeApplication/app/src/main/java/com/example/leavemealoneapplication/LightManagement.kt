package com.example.leavemealoneapplication

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.annotation.IdRes
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import com.example.leavemealoneapplication.databinding.ActivityMainBinding
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import kotlinx.coroutines.*
import nl.bryanderidder.themedtogglebuttongroup.ThemedButton
import nl.bryanderidder.themedtogglebuttongroup.ThemedToggleButtonGroup
import okhttp3.Dispatcher
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import retrofit2.Retrofit
import retrofit2.create
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

            binding.saveSetting.setOnClickListener{

                if(binding.editGoalLux.text.toString().length != 0){
                    lightEditor.putString("goalLux",binding.editGoalLux.text.toString())
                    lightEditor.apply()
                    Log.d("lightUpdate","goalLux : " + "${binding.editGoalLux.text.toString()}")
                }

                if(binding.less.isSelected == true){
                    lightEditor.putString("chlorophyll", "A")
                    lightEditor.apply()
                    Log.d("lightUpdate", "chlorophyll : A")
                }
                else if(binding.normal.isSelected == true){
                    lightEditor.putString("chlorophyll", "B")
                    lightEditor.apply()
                    Log.d("lightUpdate", "chlorophyll : B")
                }
                else{
                    lightEditor.putString("chlorophyll", "C")
                    lightEditor.apply()
                    Log.d("lightUpdate", "chlorophyll : C")
                }

                if(binding.on.id == binding.lightOnOffToggleBtn.checkedId){
                    lightEditor.putString("allowingOfAUser", "true")
                    lightEditor.apply()
                    Log.d("lightUpdate", "allowingOfAUser : true")
                }
                else if(binding.off.id == binding.lightOnOffToggleBtn.checkedId){
                    lightEditor.putString("allowingOfAUser", "false")
                    lightEditor.apply()
                    Log.d("lightUpdate", "allowingOfAUser : false")
                }

                val jsonObject = JSONObject()

                jsonObject.put("goalLux", sharedLight.getString("goalLux","0"))
                jsonObject.put("chlorophyll", sharedLight.getString("chlorophyll","A"))
                jsonObject.put("allowingOfAUser", sharedLight.getString("allowingOfAUser","true"))

                //rawJSON(jsonObject)




            }
        }
    }

    fun rawJSON(jsonObject: JSONObject) {

        //레트로핏 만들기
        val retrofit = Retrofit.Builder().baseUrl("http://192.168.219.110").build()

        //Service 만들기
        val service = retrofit.create(LightService::class.java)

        //JSONObject 이용해서 JSON 만들기
        val jsonObject = jsonObject

        //JSONObject를 String으로 컨버트
        val jsonObjectString = jsonObject.toString()

        //RequestBody 만들기. GsonConverter 같은 컨버터를 안쓰고 있으므로, RequestBody를 이용할 필요가 있다.
        val requestBody = jsonObjectString.toRequestBody("application/json".toMediaTypeOrNull())

        CoroutineScope(Dispatchers.IO).launch {

            // PUT request를 함과 동시에, response 받기.
            val response = service.updateLightSetting(requestBody)

            withContext(Dispatchers.Main) {
                // raw JSON을 GSON 라이브러리를 써서 pretty JSON으로 바꾸기
                /*if (response.isSuccessful) {
                    val gson = GsonBuilder().setPrettyPrinting().create()
                    val prettyJson = gson.toJson(JsonParser.parseString(response.body?.string()))

                    Log.d("Pretty Printed JSON : ", prettyJson)
                } else {
                    Log.e("RETROFIT_ERROR", response.code.toString())
                }*/
            }
        }
    }
}
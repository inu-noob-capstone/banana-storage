package com.example.leavemealoneapplication

import okhttp3.RequestBody
import okhttp3.Response
import okhttp3.ResponseBody
import retrofit2.http.PUT
import retrofit2.http.Body

interface LightService {
    @PUT("/lightSetting.json")
    suspend fun updateLightSetting(@Body requestBody: RequestBody): ResponseBody

}
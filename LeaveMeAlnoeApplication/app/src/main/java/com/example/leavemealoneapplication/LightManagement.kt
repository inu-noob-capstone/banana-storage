package com.example.leavemealoneapplication

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.leavemealoneapplication.databinding.ActivityMainBinding

class LightManagement : AppCompatActivity() {
    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
    }
}
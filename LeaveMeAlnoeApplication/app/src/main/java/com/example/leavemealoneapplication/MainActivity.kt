package com.example.leavemealoneapplication

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.core.widget.addTextChangedListener
import com.example.leavemealoneapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)


        var list = mutableListOf("Scope", "Function")

        val afterApply = list.let{
            it.add("Apply")
            it.count()
        }
        println("반환값 apply = $afterApply")

        val afterAlso = list.run {
            add("Also")
            count()
        }
        println("반환값 also = $afterAlso")

        val lastItemWith = with(list){
            add("With")
            get(size-1)
        }
        println("반환값 with = $lastItemWith")
    }
}

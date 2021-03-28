package com.example.leavemealoneapplication

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 접근 제한자 테스트
        var child = Child()
        child.callVariables()

        // 부모 클래스 직접 호출해보기
        var parent = Parent()
        Log.d("Visibility", "Parent: 기본 제한자 defaultVal의 값은 ${parent.defaultVal}")
        Log.d("Visibility", "Parent: internalVal의 값은 ${parent.internalVal}")
    }
}

// 추상 클래스 설계
abstract class Animal{
    fun walk(){
        Log.d("abstract", "걷습니다.")
    }
    abstract fun move()
}

// 구현
class Bird:Animal(){
    override fun move(){
        Log.d("abstract","날아서 이동합니다.")
    }
}

// interface 설계
interface InterfaceKotlin {
    var variable: String
    fun get()
    fun set()
}

//구현
class KotlinImpl: InterfaceKotlin{
    override var variable: String = "init value"
    override fun get(){
        // 코드 구현
    }
    override fun set(){
        // 코드 구현
    }
}

// 접근 제한자 테스트를 위한 부모 클래스
open class Parent{
    private val privateVal = 1
    protected open val protectedVal = 2
    internal val internalVal = 3
    val defaultVal = 4
}

// 자식 클래스
class Child: Parent(){
    fun callVariables(){
        // privateVal은 호출이 안 됩니다.
        Log.d("Visibility","Child: protected의 값은 ${protectedVal}")
        Log.d("Visibility", "Child: internalVal의 값은 ${internalVal}")
        Log.d("Visibility", "Child: 기본 제한자 defaultVal의 값은 ${defaultVal}")
    }
}
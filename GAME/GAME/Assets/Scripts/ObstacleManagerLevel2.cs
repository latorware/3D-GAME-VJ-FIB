using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleManagerLevel2 : MonoBehaviour
{
    //Nivell 2
    public Transform punxes1;
    public Transform punxes2;
    public Transform punxes3;
    public Transform punxes4;
    private float posicioInicialYPunxa1;
    private float posicioInicialYPunxa2;
    private float posicioInicialYPunxa3;
    private float posicioInicialYPunxa4;
    private bool pujantGrupPunxes1;
    public float speedGrupPunxes1Pujada;
    public float speedGrupPunxes1Baixada;
    private float rangeGrupPunxes1;



    public Transform punxes6;
    public Transform punxes7;
    public Transform punxes8;
    public Transform punxes9;
    public Transform punxes10;
    private float posicioInicialYPunxa8;
    private float posicioInicialYPunxa6;
    private float posicioInicialYPunxa10;
    private float posicioInicialYPunxa7;
    private float posicioInicialYPunxa9;
    private bool pujantGrupPunxes2;
    public float speedGrupPunxes2Pujada;
    public float speedGrupPunxes2Baixada;
    private float rangeGrupPunxes2;

    public Transform punxes11;
    private float posicioInicialYPunxa11;
    private bool pujantGrupPunxes3;
    public float speedGrupPunxes3Pujada;
    public float speedGrupPunxes3Baixada;
    private float rangeGrupPunxes3;

    public Transform Girador1;
    public float speedGirador1;

    public Transform Girador2;
    public float speedGirador2;


    //Nivell 1
    public Transform Torus1Nivell1;
    public float speedTorus1Nivell1;
    public Transform Torus2Nivell1;
    public float speedTorus2Nivell1;
    public Transform d1;
    private float posicioInicialZd1;
    bool fentEsquerrad1;
    private float ranged1;
    public float speedd1; 
    public Transform d2;
    private float posicioInicialZd2;
    bool fentEsquerrad2;
    private float ranged2; 
    public float speedd2;
    public Transform d3;
    private float posicioInicialZd3;
    bool fentEsquerrad3;
    private float ranged3; 
    public float speedd3;


    //Nivell 3
    public Transform pendulum1; 
    public float MaxAngleDeflectionPendulum1;
    public float SpeedPendulum1;
    public Transform pendulum2;
    public float MaxAngleDeflectionPendulum2;
    public float SpeedPendulum2;
    public Transform pendulum3;
    public float MaxAngleDeflectionPendulum3;
    public float SpeedPendulum3;
    public Transform pendulum4;
    public float MaxAngleDeflectionPendulum4;
    public float SpeedPendulum4;
    public Transform pendulum5;
    public float MaxAngleDeflectionPendulum5;
    public float SpeedPendulum5;
    public Transform pendulum6;
    public float MaxAngleDeflectionPendulum6;
    public float SpeedPendulum6;
    public Transform pendulum7;
    public float MaxAngleDeflectionPendulum7;
    public float SpeedPendulum7;
    public Transform aspa1;
    public float speedaspa1;
    public Transform aspa2;
    public float speedaspa2;

    //Nivell 5
    public Transform porta11;
    public float speedPorta1;
    public Transform porta12;
    public Transform porta21;
    public float speedPorta2;
    public Transform porta22;
    public Transform porta31;
    public float speedPorta3;
    public Transform porta32;
    public Transform porta41;
    public float speedPorta4;
    public Transform porta42;
    public Transform Roda1;
    public float speedRoda1;
    public Transform Roda2;
    public float speedRoda2;




    // Start is called before the first frame update
    void Start()
    {
        //Nivell 2
        posicioInicialYPunxa1 = punxes1.position.y;
        posicioInicialYPunxa2 = punxes2.position.y;
        posicioInicialYPunxa3 = punxes3.position.y;
        posicioInicialYPunxa4 = punxes4.position.y;
        pujantGrupPunxes1 = false;
        rangeGrupPunxes1 = 5f;
        StartCoroutine(MouGrupPunxes1());

        posicioInicialYPunxa8 = punxes8.position.y;
        posicioInicialYPunxa6 = punxes6.position.y;
        posicioInicialYPunxa7 = punxes7.position.y;
        posicioInicialYPunxa9 = punxes9.position.y;
        posicioInicialYPunxa10 = punxes10.position.y;
        pujantGrupPunxes2 = false;
        rangeGrupPunxes2 = 5f;
        StartCoroutine(MouGrupPunxes2());


        posicioInicialYPunxa11 = punxes11.position.y;
        pujantGrupPunxes3 = false;
        rangeGrupPunxes3 = 7f;
        StartCoroutine(MouGrupPunxes3());



        //Nivell 1
        posicioInicialZd1 = d1.localPosition.z;
        fentEsquerrad1 = true;
        ranged1 = 10f; 
        StartCoroutine (Moud1());

        posicioInicialZd2 = d2.localPosition.z;
        fentEsquerrad2 = true;
        ranged2 = 10f;
        StartCoroutine(Moud2());

        posicioInicialZd3 = d3.localPosition.z;
        fentEsquerrad3 = true;
        ranged3 = 10f;
        StartCoroutine(Moud3());


        //Nivell 5
        StartCoroutine(MouPorta2());
        porta31.Rotate(0f, -90, 0f, Space.Self);
        StartCoroutine(MouPorta4());
        StartCoroutine(MouRoda2()); 

    }

    // Update is called once per frame
    void Update()
    {
        Girador1.Rotate(0f, -speedGirador1 * Time.deltaTime, 0f, Space.Self);
        Girador2.Rotate(0f, -speedGirador2 * Time.deltaTime, 0f, Space.Self);
        Torus1Nivell1.Rotate(0f, 0f, -speedTorus1Nivell1 * Time.deltaTime, Space.Self);
        Torus2Nivell1.Rotate(0f,0f, speedTorus2Nivell1 * Time.deltaTime, Space.Self);


        //Nivell 3
        float angle = MaxAngleDeflectionPendulum1 * Mathf.Sin(Time.time * SpeedPendulum1);
        pendulum1.localRotation = Quaternion.Euler(0, 0, angle);
        angle = MaxAngleDeflectionPendulum2 * Mathf.Sin(Time.time * SpeedPendulum2);
        pendulum2.localRotation = Quaternion.Euler(0, 0, angle);
        angle = -MaxAngleDeflectionPendulum3 * Mathf.Sin(Time.time * SpeedPendulum3);
        pendulum3.localRotation = Quaternion.Euler(0, 0, angle);
        angle = MaxAngleDeflectionPendulum4 * Mathf.Sin(Time.time * SpeedPendulum4);
        pendulum4.localRotation = Quaternion.Euler(0, 0, angle);
        angle = -MaxAngleDeflectionPendulum5 * Mathf.Sin(Time.time * SpeedPendulum5);
        pendulum5.localRotation = Quaternion.Euler(0, 0, angle);
        angle = MaxAngleDeflectionPendulum6 * Mathf.Sin(Time.time * SpeedPendulum6);
        pendulum6.localRotation = Quaternion.Euler(0, 0, angle);
        angle = -MaxAngleDeflectionPendulum7 * Mathf.Sin(Time.time * SpeedPendulum7);
        pendulum7.localRotation = Quaternion.Euler(0, 0, angle);
        aspa1.Rotate(-speedaspa1 * Time.deltaTime, 0f, 0f, Space.Self);
        aspa2.Rotate(speedaspa2 * Time.deltaTime, 0f, 0f, Space.Self);

        //Nivell 5
        porta11.Rotate(0f, -speedPorta1 * Time.deltaTime, 0f, Space.Self);
        porta12.Rotate(0f, speedPorta1 * Time.deltaTime, 0f, Space.Self);

        porta31.Rotate(0f, -speedPorta3 * Time.deltaTime, 0f, Space.Self);
        porta32.Rotate(0f, speedPorta3 * Time.deltaTime, 0f, Space.Self);

        Roda1.Rotate(0f, 0f, -speedRoda1 * Time.deltaTime, Space.Self);



    }

    private IEnumerator MouGrupPunxes1()
    {
        while (true)
        {


            if ((punxes1.position.y > posicioInicialYPunxa1) && (pujantGrupPunxes1))
            {
                pujantGrupPunxes1 = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((punxes1.position.y < (posicioInicialYPunxa1 - rangeGrupPunxes1)) && (!pujantGrupPunxes1))
            {
                pujantGrupPunxes1 = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (pujantGrupPunxes1)
                {
                    punxes1.Translate(new Vector3(0f, speedGrupPunxes1Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes2.Translate(new Vector3(0f, speedGrupPunxes1Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes3.Translate(new Vector3(0f, speedGrupPunxes1Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes4.Translate(new Vector3(0f, speedGrupPunxes1Pujada * Time.deltaTime, 0f), Space.Self);
                }
                else
                {
                    punxes1.Translate(new Vector3(0f, -speedGrupPunxes1Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes2.Translate(new Vector3(0f, -speedGrupPunxes1Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes3.Translate(new Vector3(0f, -speedGrupPunxes1Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes4.Translate(new Vector3(0f, -speedGrupPunxes1Baixada * Time.deltaTime, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator MouGrupPunxes2()
    {
        while (true)
        {


            if ((punxes8.position.y > posicioInicialYPunxa8) && (pujantGrupPunxes2))
            {
                pujantGrupPunxes2 = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((punxes8.position.y < (posicioInicialYPunxa8 - rangeGrupPunxes2)) && (!pujantGrupPunxes2))
            {
                pujantGrupPunxes2 = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (pujantGrupPunxes2)
                {
                    punxes6.Translate(new Vector3(0f, speedGrupPunxes2Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes7.Translate(new Vector3(0f, speedGrupPunxes2Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes8.Translate(new Vector3(0f, speedGrupPunxes2Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes9.Translate(new Vector3(0f, speedGrupPunxes2Pujada * Time.deltaTime, 0f), Space.Self);
                    punxes10.Translate(new Vector3(0f, speedGrupPunxes2Pujada * Time.deltaTime, 0f), Space.Self);
                }
                else
                {
                    punxes6.Translate(new Vector3(0f, -speedGrupPunxes2Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes7.Translate(new Vector3(0f, -speedGrupPunxes2Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes8.Translate(new Vector3(0f, -speedGrupPunxes2Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes9.Translate(new Vector3(0f, -speedGrupPunxes2Baixada * Time.deltaTime, 0f), Space.Self);
                    punxes10.Translate(new Vector3(0f, -speedGrupPunxes2Baixada * Time.deltaTime, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator MouGrupPunxes3()
    {
        while (true)
        {


            if ((punxes11.position.y > posicioInicialYPunxa11) && (pujantGrupPunxes3))
            {
                pujantGrupPunxes3 = false;
                yield return new WaitForSeconds(0.5f);
            }
            else if ((punxes11.position.y < (posicioInicialYPunxa11 - rangeGrupPunxes3)) && (!pujantGrupPunxes3))
            {
                pujantGrupPunxes3 = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (pujantGrupPunxes3)
                {
                    punxes11.Translate(new Vector3(0f, speedGrupPunxes3Pujada * Time.deltaTime, 0f), Space.Self);
                }
                else
                {
                    punxes11.Translate(new Vector3(0f, -speedGrupPunxes3Baixada * Time.deltaTime, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator Moud1()
    {
        while (true)
        {


            if ((d1.localPosition.z > posicioInicialZd1) && (!fentEsquerrad1))
            {
                fentEsquerrad1 = true; 
                yield return new WaitForSeconds(1f);
            }
            else if ((d1.localPosition.z < (posicioInicialZd1 - ranged1)) && (fentEsquerrad1))
            {
                fentEsquerrad1 = false; 
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentEsquerrad1)
                {
                    d1.Translate(new Vector3(0f, 0f, -speedd1 * Time.deltaTime), Space.Self);
                }
                else
                {
                    d1.Translate(new Vector3(0f, 0f, +speedd1 * Time.deltaTime), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator Moud2()
    {
        while (true)
        {


            if ((d2.localPosition.z > posicioInicialZd2) && (!fentEsquerrad2))
            {
                fentEsquerrad2 = true;
                yield return new WaitForSeconds(0f);
            }
            else if ((d2.localPosition.z < (posicioInicialZd2 - ranged2)) && (fentEsquerrad2))
            {
                fentEsquerrad2 = false;
                yield return new WaitForSeconds(0f);
            }
            else
            {
                if (fentEsquerrad2)
                {
                    d2.Translate(new Vector3(0f, 0f, -speedd2 * Time.deltaTime), Space.Self);
                }
                else
                {
                    d2.Translate(new Vector3(0f, 0f, +speedd2 * Time.deltaTime), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator Moud3()
    {
        while (true)
        {


            if ((d3.localPosition.z > posicioInicialZd3) && (!fentEsquerrad3))
            {
                fentEsquerrad3 = true;
                yield return new WaitForSeconds(1f);
            }
            else if ((d3.localPosition.z < (posicioInicialZd3 - ranged3)) && (fentEsquerrad3))
            {
                fentEsquerrad3 = false;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentEsquerrad3)
                {
                    d3.Translate(new Vector3(0f, 0f, -speedd3 * Time.deltaTime), Space.Self);
                }
                else
                {
                    d3.Translate(new Vector3(0f, 0f, +speedd3 * Time.deltaTime), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private IEnumerator MouPorta2()
    {
        float angle = 0f; 
        while (true)
        {

            angle += -speedPorta2 * Time.deltaTime;
             
            if (angle < -180f)
            {
                angle = 0f;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                porta21.localRotation = Quaternion.Euler(0, angle, 0);
                porta22.localRotation = Quaternion.Euler(0, -angle, 0);
                yield return null;
            }
        }

    }

    private IEnumerator MouPorta4()
    {
        float angle = 0f;
        while (true)
        {

            angle += -speedPorta4 * Time.deltaTime;

            if (angle < -180f)
            {
                angle = 0f;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                porta41.localRotation = Quaternion.Euler(-angle, 0, 0);
                porta42.localRotation = Quaternion.Euler(-angle-90f, 0, 0);
                yield return null;
            }
        }

    }

    private IEnumerator MouRoda2()
    {
        float current = 0f;
        float angle = 0f; 
        while (true)
        {

            angle += speedRoda2 * Time.deltaTime;
            current += speedRoda2 * Time.deltaTime; 

            if (current > 45f)
            {
                current = 0f;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                Roda2.localRotation = Quaternion.Euler(0, 0, angle);
                yield return null;
            }
        }

    }
}
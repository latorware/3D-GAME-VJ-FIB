using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleManagerLevel2 : MonoBehaviour
{

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




    // Start is called before the first frame update
    void Start()
    {
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
    }

    // Update is called once per frame
    void Update()
    {
        Girador1.Rotate(0f, -speedGirador1 * Time.deltaTime, 0f, Space.Self);
        Girador2.Rotate(0f, -speedGirador2 * Time.deltaTime, 0f, Space.Self);
    }

    private IEnumerator MouGrupPunxes1()
    {
        while (true)
        {


            if ((punxes1.position.y > posicioInicialYPunxa1) && (pujantGrupPunxes1))
            {
                pujantGrupPunxes1 = false;
                //punxes1.position = new Vector3(punxes1.position.x, posicioInicialYPunxa1, punxes1.position.z);
                //punxes2.position = new Vector3(punxes2.position.x, posicioInicialYPunxa2, punxes2.position.z);
                //punxes3.position = new Vector3(punxes3.position.x, posicioInicialYPunxa3, punxes3.position.z);
                //punxes4.position = new Vector3(punxes4.position.x, posicioInicialYPunxa4, punxes4.position.z);
                yield return new WaitForSeconds(1f);
            }
            else if ((punxes1.position.y < (posicioInicialYPunxa1 - rangeGrupPunxes1)) && (!pujantGrupPunxes1))
            {
                pujantGrupPunxes1 = true;
                //punxes1.position = new Vector3(punxes1.position.x, posicioInicialYPunxa1 - rangeGrupPunxes1, punxes1.position.z);
                //punxes2.position = new Vector3(punxes2.position.x, posicioInicialYPunxa2 - rangeGrupPunxes1, punxes2.position.z);
                //punxes3.position = new Vector3(punxes3.position.x, posicioInicialYPunxa3 - rangeGrupPunxes1, punxes3.position.z);
                //punxes4.position = new Vector3(punxes4.position.x, posicioInicialYPunxa4 - rangeGrupPunxes1, punxes4.position.z);
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
                //punxes6.position = new Vector3(punxes6.position.x, posicioInicialYPunxa6, punxes6.position.z);
                //punxes7.position = new Vector3(punxes7.position.x, posicioInicialYPunxa7, punxes7.position.z);
                //punxes8.position = new Vector3(punxes8.position.x, posicioInicialYPunxa8, punxes8.position.z);
                //punxes9.position = new Vector3(punxes9.position.x, posicioInicialYPunxa9, punxes9.position.z);
                //punxes10.position = new Vector3(punxes10.position.x, posicioInicialYPunxa10, punxes10.position.z);
                yield return new WaitForSeconds(1f);
            }
            else if ((punxes8.position.y < (posicioInicialYPunxa8 - rangeGrupPunxes2)) && (!pujantGrupPunxes2))
            {
                pujantGrupPunxes2 = true;
                //punxes6.position = new Vector3(punxes6.position.x, posicioInicialYPunxa6 - rangeGrupPunxes2, punxes6.position.z);
                //punxes7.position = new Vector3(punxes7.position.x, posicioInicialYPunxa7 - rangeGrupPunxes2, punxes7.position.z);
                //punxes8.position = new Vector3(punxes8.position.x, posicioInicialYPunxa8 - rangeGrupPunxes2, punxes8.position.z);
                //punxes9.position = new Vector3(punxes9.position.x, posicioInicialYPunxa9 - rangeGrupPunxes2, punxes9.position.z);
                //punxes10.position = new Vector3(punxes10.position.x, posicioInicialYPunxa10 - rangeGrupPunxes2, punxes10.position.z);
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
                //punxes11.position = new Vector3(punxes11.position.x, posicioInicialYPunxa11, punxes11.position.z);
                yield return new WaitForSeconds(0.5f);
            }
            else if ((punxes11.position.y < (posicioInicialYPunxa11 - rangeGrupPunxes3)) && (!pujantGrupPunxes3))
            {
                pujantGrupPunxes3 = true;
                //punxes11.position = new Vector3(punxes11.position.x, posicioInicialYPunxa11 - rangeGrupPunxes3, punxes11.position.z);
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
}
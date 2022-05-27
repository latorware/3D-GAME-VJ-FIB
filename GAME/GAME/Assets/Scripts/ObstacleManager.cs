using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleManager : MonoBehaviour
{
    public GlobalVolumeManager volumeManager;


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
    public Transform d8;
    private float posicioInicialZd8;
    bool fentEsquerrad8;
    private float ranged8;
    public float speedd8;
    public Transform Girador3;
    public float speedGirador3;

    //Nivell 4
    public Transform martell1;
    public float speedmartell1;
    public Transform martell2;
    public float speedmartell2;
    public Transform martell3;
    public float speedmartell3;
    public Transform martell4;
    public float speedmartell4;
    public Transform martell5;
    public float speedmartell5;
    public Transform martell6;
    public float speedmartell6;
    public Transform martell7;
    public float speedmartell7;
    public Transform martell8;
    public float speedmartell8;
    public Transform Torus3;
    public float speedTorus3;
    public Transform aspa3;
    public float speedaspa3;
    public Transform aspa4;
    public float speedaspa4;
    public Transform Boxa1; 
    public float speedboxa1;
    public Transform Boxa2;
    public float speedboxa2;
    public Transform Boxa3;
    public float speedboxa3;
    public Transform Boxa4;
    public float speedboxa4;


    //Invulnerabilitat
    bool invulnerable;
    public MeshCollider Torus1Collider;
    public MeshCollider Torus2Collider;
    public CapsuleCollider punxes1Colider; 
    public CapsuleCollider punxes2Colider;
    public CapsuleCollider punxes3Colider;
    public CapsuleCollider punxes4Colider;
    public BoxCollider punxes8Colider;
    public BoxCollider punxes11Colider;
    public CapsuleCollider cGran1Colider;
    public CapsuleCollider cGran2Colider;
    public BoxCollider d2Colider;
    public BoxCollider d1Colider;
    public BoxCollider d3Colider;
    public SphereCollider f11Colider;
    public SphereCollider f22Colider;
    public SphereCollider f33Colider;
    public SphereCollider f44Colider;
    public SphereCollider f55Colider;
    public SphereCollider f66Colider;
    public SphereCollider f77Colider;
    public BoxCollider pal2aspa1Colider;
    public BoxCollider pal1aspa1Colider;
    public BoxCollider pal1aspa2Colider;
    public BoxCollider pal2aspa2Colider;
    public BoxCollider porta11Colider;
    public BoxCollider porta12Colider;
    public BoxCollider porta21Colider;
    public BoxCollider porta22Colider;
    public BoxCollider porta31Colider;
    public BoxCollider porta32Colider;
    public BoxCollider porta41Colider;
    public BoxCollider porta42Colider;
    public MeshCollider Roda1Objecte1Colider;
    public MeshCollider Roda1Objecte2Colider;
    public MeshCollider Roda1Objecte3Colider;
    public MeshCollider Roda1Objecte4Colider;
    public MeshCollider Roda4Objecte1Colider;
    public MeshCollider Roda4Objecte2Colider;
    public MeshCollider Roda4Objecte3Colider;
    public MeshCollider Roda4Objecte4Colider;
    public BoxCollider d8Colider;
    public CapsuleCollider cGran3Collider;
    public BoxCollider picMartell1Colider;
    public BoxCollider picMartell2Colider;
    public BoxCollider picMartell3Colider;
    public BoxCollider picMartell4Colider;
    public BoxCollider picMartell5Colider;
    public BoxCollider picMartell6Colider;
    public BoxCollider picMartell7Colider;
    public BoxCollider picMartell8Colider;
    public BoxCollider pal2aspa3Colider;
    public BoxCollider pal1aspa3Colider;
    public BoxCollider pal2aspa4Colider;
    public BoxCollider pal1aspa4Colider;
    public MeshCollider Torus3Colider;
    public BoxCollider picoBoxa1Colider;
    public BoxCollider picoBoxa2Colider;
    public BoxCollider picoBoxa3Colider;
    public BoxCollider picoBoxa4Colider;
    public AudioSource magicTecles; 






    // Start is called before the first frame update
    void Start()
    {
        invulnerable = false; 
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
        posicioInicialZd8 = d8.localPosition.z;
        fentEsquerrad8 = true;
        ranged8 = 10f;
        StartCoroutine(Moud8());

        //Nivell 4
        StartCoroutine(MouMartell1());
        StartCoroutine(MouMartell2());
        StartCoroutine(MouMartell3());
        StartCoroutine(MouMartell4());
        StartCoroutine(MouMartell5());
        StartCoroutine(MouMartell6());
        StartCoroutine(MouMartell7());
        StartCoroutine(MouMartell8());
        StartCoroutine(MouBoxa4());
        StartCoroutine(MouBoxa2());
        StartCoroutine(MouBoxa3());
        StartCoroutine(MouBoxa1());

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


        //Nivell 4
        Torus3.Rotate(0f, 0f, -speedTorus3 * Time.deltaTime, Space.Self);
        aspa3.Rotate(-speedaspa3 * Time.deltaTime, 0f, 0f, Space.Self);
        aspa4.Rotate(-speedaspa4 * Time.deltaTime, 0f, 0f, Space.Self);



        //Nivell 5
        porta11.Rotate(0f, -speedPorta1 * Time.deltaTime, 0f, Space.Self);
        porta12.Rotate(0f, speedPorta1 * Time.deltaTime, 0f, Space.Self);

        porta31.Rotate(0f, -speedPorta3 * Time.deltaTime, 0f, Space.Self);
        porta32.Rotate(0f, speedPorta3 * Time.deltaTime, 0f, Space.Self);

        Roda1.Rotate(0f, 0f, -speedRoda1 * Time.deltaTime, Space.Self);
        Girador3.Rotate(0f, speedGirador3 * Time.deltaTime, 0f, Space.Self);




        //Lo de la invulnerabilitat
        if (Input.GetKeyDown(KeyCode.G))
        {
            magicTecles.Play(); 
            if (!invulnerable)
            {
                invulnerable = true;
                volumeManager.BlancINegre();
                treuColiders(); 
            }
            else
            {
                invulnerable = false;
                volumeManager.Color();
                posaColiders(); 
            }
        }


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
                Roda2.localRotation = Quaternion.Euler(90, 0, angle);
                yield return null;
            }
        }
        
    }

    private IEnumerator Moud8()
    {
        while (true)
        {


            if ((d8.localPosition.z > posicioInicialZd8) && (!fentEsquerrad8))
            {
                fentEsquerrad8 = true;
                yield return new WaitForSeconds(1f);
            }
            else if ((d8.localPosition.z < (posicioInicialZd8 - ranged8)) && (fentEsquerrad8))
            {
                fentEsquerrad8 = false;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentEsquerrad8)
                {
                    d8.Translate(new Vector3(0f, 0f, -speedd8 * Time.deltaTime), Space.Self);
                }
                else
                {
                    d8.Translate(new Vector3(0f, 0f, +speedd8 * Time.deltaTime), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }



    private IEnumerator MouMartell1()
    {
        float angle = 0f;
        bool fentdalt = true; 
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell1 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(1f);
                }
                else
                {
                    martell1.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null; 
                }
            }
            else
            {
                angle += speedmartell1 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(1f);
                }
                else
                {
                    martell1.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null; 
                }
            }
        }

    }

    private IEnumerator MouMartell2()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell2 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(1f);
                }
                else
                {
                    martell2.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell2 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(1f);
                }
                else
                {
                    martell2.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell3()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell3 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell3.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell3 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell3.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell4()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell4 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell4.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell4 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell4.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell5()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell5 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell5.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell5 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell5.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell6()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell6 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell6.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell6 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0.5f);
                }
                else
                {
                    martell6.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell7()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell7 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell7.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell7 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell7.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouMartell8()
    {
        float angle = 0f;
        bool fentdalt = true;
        while (true)
        {

            if (fentdalt)
            {
                angle += -speedmartell8 * Time.deltaTime;
                if (angle < -90f)
                {
                    fentdalt = false;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell8.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
            else
            {
                angle += speedmartell8 * Time.deltaTime;

                if (angle > 0f)
                {
                    fentdalt = true;
                    yield return new WaitForSeconds(0f);
                }
                else
                {
                    martell8.localRotation = Quaternion.Euler(0, 0, angle);
                    yield return null;
                }
            }
        }

    }

    private IEnumerator MouBoxa4()
    {
        bool fentFora = false;
        float posicioInicialBoxa4X = Boxa4.localPosition.x;
        float range = 4f;
        while (true)
        {

            if ((Boxa4.localPosition.x > (posicioInicialBoxa4X + range)) && (fentFora))
            {
                fentFora = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((Boxa4.localPosition.x < (posicioInicialBoxa4X)) && (!fentFora))
            {
                fentFora = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentFora)
                {
                    Boxa4.Translate(new Vector3(speedboxa4 * Time.deltaTime, 0f, 0f), Space.Self);
                }
                else
                {
                    Boxa4.Translate(new Vector3(-speedboxa4 * Time.deltaTime, 0f, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }

    private IEnumerator MouBoxa3()
    {
        bool fentFora = false;
        float posicioInicialBoxa3X = Boxa3.localPosition.x;
        float range = 4f;
        while (true)
        {

            if ((Boxa3.localPosition.x > (posicioInicialBoxa3X + range)) && (fentFora))
            {
                fentFora = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((Boxa3.localPosition.x < (posicioInicialBoxa3X)) && (!fentFora))
            {
                fentFora = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentFora)
                {
                    Boxa3.Translate(new Vector3(speedboxa3 * Time.deltaTime, 0f, 0f), Space.Self);
                }
                else
                {
                    Boxa3.Translate(new Vector3(-speedboxa3 * Time.deltaTime, 0f, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }

    private IEnumerator MouBoxa2()
    {
        bool fentFora = true;
        float range = 4f;
        float posicioInicialBoxa2X = Boxa2.localPosition.x + range;
        while (true)
        {
            if ((Boxa2.localPosition.x < (posicioInicialBoxa2X - range)) && (fentFora))
            {
                fentFora = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((Boxa2.localPosition.x > (posicioInicialBoxa2X)) && (!fentFora))
            {
                fentFora = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentFora)
                {
                    Boxa2.Translate(new Vector3(speedboxa2 * Time.deltaTime, 0f, 0f), Space.Self);
                }
                else
                {
                    Boxa2.Translate(new Vector3(-speedboxa2 * Time.deltaTime, 0f, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }

    private IEnumerator MouBoxa1()
    {
        bool fentFora = true;
        float range = 4f;
        float posicioInicialBoxa1X = Boxa1.localPosition.x + range;
        while (true)
        {
            if ((Boxa1.localPosition.x < (posicioInicialBoxa1X - range)) && (fentFora))
            {
                fentFora = false;
                yield return new WaitForSeconds(1f);
            }
            else if ((Boxa1.localPosition.x > (posicioInicialBoxa1X)) && (!fentFora))
            {
                fentFora = true;
                yield return new WaitForSeconds(1f);
            }
            else
            {
                if (fentFora)
                {
                    Boxa1.Translate(new Vector3(speedboxa1 * Time.deltaTime, 0f, 0f), Space.Self);
                }
                else
                {
                    Boxa1.Translate(new Vector3(-speedboxa1 * Time.deltaTime, 0f, 0f), Space.Self);
                }
            }
            yield return new WaitForSeconds(0f);
        }

    }


    private void treuColiders()
    {
        Torus1Collider.enabled = false; 
        Torus2Collider.enabled = false; 
        punxes1Colider.enabled = false; 
        punxes2Colider.enabled = false; 
        punxes3Colider.enabled = false; 
        punxes4Colider.enabled = false; 
        punxes8Colider.enabled = false; 
        punxes11Colider.enabled = false; 
        cGran1Colider.enabled = false; 
        cGran2Colider.enabled = false; 
        d2Colider.enabled = false;
        d1Colider.enabled = false; 
        d3Colider.enabled = false; 
        f11Colider.enabled = false; 
        f22Colider.enabled = false; 
        f33Colider.enabled = false; 
        f44Colider.enabled = false; 
        f55Colider.enabled = false; 
        f66Colider.enabled = false;
        f77Colider.enabled = false; 
        pal2aspa1Colider.enabled = false;
        pal1aspa1Colider.enabled = false; 
        pal1aspa2Colider.enabled = false; 
        pal2aspa2Colider.enabled = false; 
        porta11Colider.enabled = false; 
        porta12Colider.enabled = false; 
        porta21Colider.enabled = false; 
        porta22Colider.enabled = false; 
        porta31Colider.enabled = false; 
        porta32Colider.enabled = false; 
        porta41Colider.enabled = false; 
        porta42Colider.enabled = false; 
        Roda1Objecte1Colider.enabled = false; 
        Roda1Objecte2Colider.enabled = false; 
        Roda1Objecte3Colider.enabled = false; 
        Roda1Objecte4Colider.enabled = false; 
        Roda4Objecte1Colider.enabled = false; 
        Roda4Objecte2Colider.enabled = false; 
        Roda4Objecte3Colider.enabled = false; 
        Roda4Objecte4Colider.enabled = false;
        d8Colider.enabled = false; 
        cGran3Collider.enabled = false; 
        picMartell1Colider.enabled = false; 
        picMartell2Colider.enabled = false; 
        picMartell3Colider.enabled = false; 
        picMartell5Colider.enabled = false; 
        picMartell6Colider.enabled = false; 
        picMartell7Colider.enabled = false; 
        picMartell8Colider.enabled = false; 
        pal2aspa3Colider.enabled = false; 
        pal1aspa3Colider.enabled = false; 
        pal2aspa4Colider.enabled = false; 
        pal1aspa4Colider.enabled = false; 
        Torus3Colider.enabled = false; 
        picoBoxa1Colider.enabled = false; 
        picoBoxa2Colider.enabled = false; 
        picoBoxa3Colider.enabled = false; 
        picoBoxa4Colider.enabled = false; 
    }

    private void posaColiders()
    {
        Torus1Collider.enabled = true; 
        Torus2Collider.enabled = true; 
        punxes1Colider.enabled = true; 
        punxes2Colider.enabled = true; 
        punxes3Colider.enabled = true; 
        punxes4Colider.enabled = true; 
        punxes8Colider.enabled = true; 
        punxes11Colider.enabled = true; 
        cGran1Colider.enabled = true; 
        cGran2Colider.enabled = true; 
        d2Colider.enabled = true;
        d1Colider.enabled = true; 
        d3Colider.enabled = true; 
        f11Colider.enabled = true; 
        f22Colider.enabled = true; 
        f33Colider.enabled = true; 
        f44Colider.enabled = true; 
        f55Colider.enabled = true; 
        f66Colider.enabled = true;
        f77Colider.enabled = true; 
        pal2aspa1Colider.enabled = true;
        pal1aspa1Colider.enabled = true; 
        pal1aspa2Colider.enabled = true; 
        pal2aspa2Colider.enabled = true; 
        porta11Colider.enabled = true; 
        porta12Colider.enabled = true; 
        porta21Colider.enabled = true; 
        porta22Colider.enabled = true; 
        porta31Colider.enabled = true; 
        porta32Colider.enabled = true; 
        porta41Colider.enabled = true; 
        porta42Colider.enabled = true; 
        Roda1Objecte1Colider.enabled = true; 
        Roda1Objecte2Colider.enabled = true; 
        Roda1Objecte3Colider.enabled = true; 
        Roda1Objecte4Colider.enabled = true; 
        Roda4Objecte1Colider.enabled = true; 
        Roda4Objecte2Colider.enabled = true; 
        Roda4Objecte3Colider.enabled = true; 
        Roda4Objecte4Colider.enabled = true;
        d8Colider.enabled = true; 
        cGran3Collider.enabled = true; 
        picMartell1Colider.enabled = true; 
        picMartell2Colider.enabled = true; 
        picMartell3Colider.enabled = true; 
        picMartell5Colider.enabled = true; 
        picMartell6Colider.enabled = true; 
        picMartell7Colider.enabled = true; 
        picMartell8Colider.enabled = true; 
        pal2aspa3Colider.enabled = true; 
        pal1aspa3Colider.enabled = true; 
        pal2aspa4Colider.enabled = true; 
        pal1aspa4Colider.enabled = true; 
        Torus3Colider.enabled = true; 
        picoBoxa1Colider.enabled = true; 
        picoBoxa2Colider.enabled = true; 
        picoBoxa3Colider.enabled = true; 
        picoBoxa4Colider.enabled = true; 
    }

}
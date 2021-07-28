from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
import sklearn


app = Flask(__name__)

columns_list = ['Year', 'Mileage', 'State_new_ AL', 'State_new_ AZ', 'State_new_ CA', 'State_new_ CO', 'State_new_ FL', 'State_new_ GA', 'State_new_ IL', 'State_new_ IN', 'State_new_ KY', 'State_new_ MA', 'State_new_ MD', 'State_new_ MI', 'State_new_ MN', 'State_new_ MO', 'State_new_ NC', 'State_new_ NJ', 'State_new_ NY', 'State_new_ OH', 'State_new_ PA', 'State_new_ TN', 'State_new_ TX', 'State_new_ VA', 'State_new_ WA', 'State_new_ WI', 'State_new_OTRO', 'Make_new_BMW', 'Make_new_Chevrolet', 'Make_new_Dodge', 'Make_new_Ford', 'Make_new_GMC', 'Make_new_Honda', 'Make_new_Hyundai', 'Make_new_Jeep', 'Make_new_Kia', 'Make_new_Lexus', 'Make_new_OTRO', 'Make_new_Toyota', 'Make_new_Volkswagen', 'Model_new_15004WD', 'Model_new_200Limited', 'Model_new_200S', 'Model_new_25004WD', 'Model_new_3', 'Model_new_300300C', 'Model_new_300300S', 'Model_new_3004dr', 'Model_new_4Runner4WD', 'Model_new_4RunnerSR5', 'Model_new_5', 'Model_new_6', 'Model_new_7', 'Model_new_AcadiaAWD', 'Model_new_AcadiaFWD', 'Model_new_Accord', 'Model_new_AccordEX-L', 'Model_new_AccordLX', 'Model_new_Altima4dr', 'Model_new_AvalonXLE', 'Model_new_C-Class4dr', 'Model_new_C-ClassC', 'Model_new_C-ClassC300', 'Model_new_CC4dr', 'Model_new_CR-V2WD', 'Model_new_CR-V4WD', 'Model_new_CR-VEX', 'Model_new_CR-VEX-L', 'Model_new_CR-VLX', 'Model_new_CTS', 'Model_new_Camaro2dr', 'Model_new_CamaroConvertible', 'Model_new_CamaroCoupe', 'Model_new_Camry', 'Model_new_Camry4dr', 'Model_new_CamryL', 'Model_new_CamryLE', 'Model_new_CamrySE', 'Model_new_CamryXLE', 'Model_new_CanyonCrew', 'Model_new_Challenger2dr', 'Model_new_ChallengerR/T', 'Model_new_Charger4dr', 'Model_new_ChargerSE', 'Model_new_ChargerSXT', 'Model_new_CherokeeLimited', 'Model_new_Civic', 'Model_new_CivicEX', 'Model_new_CivicLX', 'Model_new_ColoradoCrew', 'Model_new_CompassLatitude', 'Model_new_CompassSport', 'Model_new_Cooper', 'Model_new_Corolla4dr', 'Model_new_CorollaL', 'Model_new_CorollaLE', 'Model_new_CorollaS', 'Model_new_Corvette2dr', 'Model_new_CruzeSedan', 'Model_new_Durango2WD', 'Model_new_DurangoAWD', 'Model_new_E-ClassE', 'Model_new_E-ClassE350', 'Model_new_ES', 'Model_new_ESES', 'Model_new_Econoline', 'Model_new_EdgeLimited', 'Model_new_EdgeSEL', 'Model_new_Elantra', 'Model_new_Elantra4dr', 'Model_new_ElantraLimited', 'Model_new_EnclaveLeather', 'Model_new_EnclavePremium', 'Model_new_EquinoxAWD', 'Model_new_EquinoxFWD', 'Model_new_Escalade', 'Model_new_Escape4WD', 'Model_new_EscapeFWD', 'Model_new_EscapeSE', 'Model_new_Expedition', 'Model_new_Explorer4WD', 'Model_new_ExplorerFWD', 'Model_new_ExplorerLimited', 'Model_new_ExplorerXLT', 'Model_new_Express', 'Model_new_F-1502WD', 'Model_new_F-1504WD', 'Model_new_F-150FX4', 'Model_new_F-150Lariat', 'Model_new_F-150Platinum', 'Model_new_F-150SuperCrew', 'Model_new_F-150XL', 'Model_new_F-150XLT', 'Model_new_F-250Lariat', 'Model_new_FJ', 'Model_new_FiestaSE', 'Model_new_FlexSEL', 'Model_new_Focus4dr', 'Model_new_FocusSE', 'Model_new_ForteEX', 'Model_new_ForteLX', 'Model_new_Fusion4dr', 'Model_new_FusionHybrid', 'Model_new_FusionSE', 'Model_new_G35', 'Model_new_G37', 'Model_new_GS', 'Model_new_GSGS', 'Model_new_GX', 'Model_new_Golf', 'Model_new_Grand', 'Model_new_HighlanderFWD', 'Model_new_HighlanderLimited', 'Model_new_IS', 'Model_new_ISIS', 'Model_new_Impala4dr', 'Model_new_ImpalaLT', 'Model_new_Impreza', 'Model_new_Jetta', 'Model_new_JourneyFWD', 'Model_new_JourneySXT', 'Model_new_LS', 'Model_new_LaCrosse4dr', 'Model_new_LaCrosseFWD', 'Model_new_Legacy2.5i', 'Model_new_Liberty4WD', 'Model_new_M-ClassML350', 'Model_new_MDXAWD', 'Model_new_Malibu', 'Model_new_Malibu1LT', 'Model_new_Malibu4dr', 'Model_new_MalibuLS', 'Model_new_MalibuLT', 'Model_new_Maxima4dr', 'Model_new_Murano2WD', 'Model_new_MuranoAWD', 'Model_new_Mustang2dr', 'Model_new_MustangBase', 'Model_new_MustangGT', 'Model_new_OTRO', 'Model_new_OdysseyEX-L', 'Model_new_OdysseyTouring', 'Model_new_OptimaEX', 'Model_new_OptimaLX', 'Model_new_OptimaSX', 'Model_new_Outback2.5i', 'Model_new_Outlander', 'Model_new_Passat4dr', 'Model_new_Pathfinder4WD', 'Model_new_PathfinderS', 'Model_new_PatriotLatitude', 'Model_new_PatriotSport', 'Model_new_Pilot2WD', 'Model_new_Pilot4WD', 'Model_new_PilotEX-L', 'Model_new_PilotTouring', 'Model_new_Prius', 'Model_new_Prius5dr', 'Model_new_PriusThree', 'Model_new_PriusTwo', 'Model_new_RAV44WD', 'Model_new_RAV4FWD', 'Model_new_RAV4LE', 'Model_new_RAV4Limited', 'Model_new_RAV4XLE', 'Model_new_RDXAWD', 'Model_new_RX', 'Model_new_RXRX', 'Model_new_Ram', 'Model_new_Rover', 'Model_new_S60T5', 'Model_new_SRXLuxury', 'Model_new_Santa', 'Model_new_SedonaLX', 'Model_new_Sentra4dr', 'Model_new_Sienna5dr', 'Model_new_SiennaLE', 'Model_new_SiennaXLE', 'Model_new_Sierra', 'Model_new_Silverado', 'Model_new_Sonata4dr', 'Model_new_SonataLimited', 'Model_new_SonataSE', 'Model_new_SonicSedan', 'Model_new_SorentoEX', 'Model_new_SorentoLX', 'Model_new_Soul+', 'Model_new_SoulBase', 'Model_new_SportageLX', 'Model_new_Suburban2WD', 'Model_new_Suburban4WD', 'Model_new_Super', 'Model_new_Tacoma2WD', 'Model_new_Tacoma4WD', 'Model_new_TacomaBase', 'Model_new_TacomaPreRunner', 'Model_new_Tahoe2WD', 'Model_new_Tahoe4WD', 'Model_new_TahoeLT', 'Model_new_TaurusSEL', 'Model_new_TerrainAWD', 'Model_new_TerrainFWD', 'Model_new_Town', 'Model_new_Transit', 'Model_new_TraverseAWD', 'Model_new_TraverseFWD', 'Model_new_TucsonAWD', 'Model_new_TucsonFWD', 'Model_new_Tundra', 'Model_new_TundraSR5', 'Model_new_Wrangler', 'Model_new_Wrangler4WD', 'Model_new_WranglerSport', 'Model_new_X3xDrive28i', 'Model_new_X5AWD', 'Model_new_X5xDrive35i', 'Model_new_Yukon', 'Model_new_Yukon2WD', 'Model_new_Yukon4WD']

def load_values(year, mileage, state, make, model):
    df = pd.DataFrame(np.zeros((1, len(columns_list))), columns=columns_list).astype(int)
    state_col = 'State_ ' + state
    make_col = 'Make_' + make
    model_col = 'Model_' + model
    # Se asignan los valores a el dataframe
    df.at[0,'Year'] = year
    df.at[0,'Mileage'] = mileage
    if state_col in columns_list:
        df.at[0,state_col] = 1
    else:
        df.at[0, 'State_new_OTRO'] = 1
    if make_col in columns_list:
        df.at[0,make_col] = 1
    else:
        df.at[0, 'Make_new_OTRO'] = 1

    if model_col in columns_list:
        df.at[0,model_col] = 1
    else:
        df.at[0, 'Model_new_OTRO'] = 1

    print('DF:')
    print(df)
    return df


def predict(data):
    file = open('p2_model', 'rb')
    model = pickle.load(file)
    return model.predict(data.values)[0]


@app.route('/predict', methods = ['GET'])
def URL_predict():
    year = request.args.get('YEAR')
    mileage = request.args.get('MILEAGE')
    state = request.args.get('STATE')
    make = request.args.get('MAKE')
    model = request.args.get('MODEL')

    df_values = load_values(year, mileage, state, make, model)

    pd = predict(df_values)

    return 'Su auto tiene un valor de:  ' + str(pd)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host= '0.0.0.0', port = 8888)



# 127.0.0.1:8080/predict?YEAR=2021&MILEAGE=1000&STATE=FL&MAKE=Jeep&MODEL=Wrangler
# 127.0.0.1:8888/predict?YEAR=2016&MILEAGE=25741&STATE=FL&MAKE=Chevrolet&MODEL=CamaroCoupe
